import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Optional, Set, Type, TypeVar, Union

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from pait.app.any.util import import_func_from_app
from pait.core import Pait
from pait.model.tag import Tag
from pait.util import get_func_param_kwargs

from grpc_gateway.rebuild_message import rebuild_dict

MessageT = TypeVar("MessageT", bound=Message)
ConfigT = TypeVar("ConfigT", bound="BaseGrpcGatewayRouteConfig")

__all__ = ["BaseGrpcGatewayRoute", "BaseGrpcGatewayRouteConfig"]
_grpc_gateway_title_set: Set[str] = set()


@dataclass
class BaseGrpcGatewayRouteConfig(object):
    # The way to parse protobuf message, see the specific usage method：
    #  https://github.com/so1n/protobuf_to_pydantic#23parameter-verification
    parse_msg_desc: Optional[str] = None
    #  url prefix
    prefix: str = ""
    # Title of gRPC Gateway, if there are multiple gRPC Gateways in the same Stub,
    #  need to ensure that the title of each gRPC Gateway is different
    title: str = ""
    # protobuf.json_format.msg_to_dict func
    msg_to_dict: Callable = MessageToDict
    # protobuf.json_format.parse_dict func
    parse_dict: Optional[Callable] = None
    # instance of pait
    pait: Optional[Pait] = None
    # The method of converting Message to Response object
    make_response: Optional[Callable] = None
    # A function that registers multiple routes with the app
    add_multi_simple_route: Optional[Callable] = None
    # Extended parameters supported by the `add multi simple route` function of different frameworks
    kwargs_param: Optional[Dict[str, Any]] = None


class BaseGrpcGatewayRoute(Generic[ConfigT]):
    pait: Pait
    add_multi_simple_route: staticmethod
    channel: Union[grpc.Channel, grpc.aio.Channel]

    _make_response: staticmethod = staticmethod(lambda x: x)
    _grpc_tag: Tag = Tag("grpc", desc="grpc route")

    def __init__(self, app: Any, config: Optional[ConfigT] = None):
        """
        :param app: Instance object of the web framework
        :param config: GrpcGatewayRoute Config
        """
        self.config: ConfigT = config or BaseGrpcGatewayRouteConfig()  # type: ignore[assignment]
        if self.config.title in _grpc_gateway_title_set:
            raise ValueError(f"grpc gateway title: {self.config.title} already exists")
        _grpc_gateway_title_set.add(self.config.title)

        self.app: Any = app
        # If empty, try to get an available Pait
        self._pait: Pait = (
            self.config.pait or getattr(self, "pait", None) or import_func_from_app("pait", app=app)
        )  # type: ignore
        self._add_multi_simple_route = (
            self.config.add_multi_simple_route
            or getattr(self, "add_multi_simple_route", None)
            or import_func_from_app("add_multi_simple_route", app=app)
        )  # type: ignore
        self.make_response: Callable = self.config.make_response or self._make_response
        self._tag_dict: Dict[str, Tag] = {}

        # First use inspect to get the function signature of add_multi_simple_route,
        # and then generate a dictionary containing the function signature of add_multi_simple_route through kwargs
        self._add_multi_simple_route_kwargs = (
            get_func_param_kwargs(self._add_multi_simple_route, self.config.kwargs_param)
            if self.config.kwargs_param
            else self.config.kwargs_param
        ) or {}

    @staticmethod
    def check_event_loop(grpc_func: Callable) -> None:
        """Check whether the event loop of the channel is the same as that of the app"""
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        if loop != getattr(grpc_func, "_loop", None):
            raise RuntimeError(
                "Loop is not same, "
                "the grpc channel must be initialized after the event loop of the api server is initialized"
            )

    def get_msg_from_dict(self, msg: Type[MessageT], request_dict: dict) -> MessageT:
        """Convert the Json data to the grpc Message object"""
        if self.config.parse_dict:
            request_msg: MessageT = self.config.parse_dict(request_dict, msg())
        else:
            request_msg = msg(**request_dict)  # type: ignore
        return request_msg

    def msg_from_dict_handle(self, msg: Type[MessageT], request_dict: dict, nested: Optional[list] = None) -> MessageT:
        """
        Desc:
            Http Request Dict to gRPC request protobuf Message
        e.g:
            message = {
                "a": {
                    "b": {
                        "column1": 1,
                        "column2": "demo"
                    }
                }
            }

            request_dict = {
                "column1": 1,
                "column2": "demo"
            }

            If you want to convert request dict to message object, need to specify nested=["a", "b"]

        :param msg: protobuf Message class
        :param request_dict: request dict
        :param nested: If the request dict is nested, you need to specify the column name of the nested dict
        :return: protobuf Message
        """
        if nested:
            for column in nested:
                request_dict = {column: request_dict}
        return self.get_msg_from_dict(msg, request_dict)

    def msg_to_dict_handle(
        self, message: Message, exclude_column_name: Optional[list] = None, nested: Optional[list] = None
    ) -> dict:
        """
        Desc:
            gRPC response protobuf Message to HTTP response dict
        e.g:
            - 1:
                message = { "a": 1, "b": 2, "c": 3 } and exclude = ["a", "b"]

                return value is {"c": 3}

            - 2:
                message = {
                    "a": {
                        "b": {
                            "column1": 1,
                            "column2": "demo"
                        }
                    }
                } and nested = ["a", "b"]

                return value is {
                    "column1": 1,
                    "column2": "demo"
                }

        :param message: gRPC response protobuf Message
        :param exclude_column_name: Exclude column name
        :param nested: If the response dict is nested, you need to specify the column name of the nested dict
        :return: HTTP response dict
        """
        message_dict = self.config.msg_to_dict(message)
        if exclude_column_name or nested:
            message_dict = rebuild_dict(
                message_dict,
                exclude_column_name=exclude_column_name,
                nested=nested,
            )
        return self.make_response(message_dict)

    def reinit_channel(
        self, channel: Union[grpc.Channel, grpc.aio.Channel], auto_close: bool = False
    ) -> Union[grpc.Channel, grpc.aio.Channel, None]:
        """Use the new channel (if the old channel already exists, it will be replaced and returned)

        :param channel: grpc client channel
        :param auto_close: If True, already existing channels are closed and returned.
            Otherwise, only channels that have not been closed are returned
        """
        old_channel: Union[grpc.Channel, grpc.aio.Channel, None] = getattr(self, "channel", None)
        self.channel = channel
        # If it is grpc.aio.Channel, it will return the corresponding grpc.Channel first,
        # and then close it asynchronously
        if old_channel and auto_close:
            old_channel.close()
        return old_channel

    def init_channel(self, channel: Union[grpc.Channel, grpc.aio.Channel]) -> None:
        self.reinit_channel(channel, auto_close=True)
