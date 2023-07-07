import inspect
from typing import Any, Callable, Dict, Optional, Set, Type, TypeVar, Union

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from pait.app.any.util import import_func_from_app
from pait.core import Pait
from pait.model import Tag

from grpc_gateway.rebuild_message import rebuild_dict

MessageT = TypeVar("MessageT", bound=Message)

__all__ = ["BaseGrpcGatewayRoute"]
_grpc_gateway_title_set: Set[str] = set()


class BaseGrpcGatewayRoute(object):
    pait: Pait
    _make_response: staticmethod = staticmethod(lambda x: x)
    add_multi_simple_route: staticmethod
    channel: Union[grpc.Channel, grpc.aio.Channel]

    _grpc_tag: Tag = Tag("grpc", desc="grpc route")

    def __init__(
        self,
        app: Any,
        parse_msg_desc: Optional[str] = None,
        prefix: str = "",
        title: str = "",
        msg_to_dict: Callable = MessageToDict,
        parse_dict: Optional[Callable] = None,
        pait: Optional[Pait] = None,
        make_response: Optional[Callable] = None,
        add_multi_simple_route: Optional[Callable] = None,
        **kwargs: Any,
    ):
        """
        :param app: Instance object of the web framework
        :param parse_msg_desc: The way to parse protobuf message, see the specific usage method：
            https://github.com/so1n/protobuf_to_pydantic#23parameter-verification
        :param prefix: url prefix
        :param title: Title of gRPC Gateway, if there are multiple gRPC Gateways in the same Stub,
            you need to ensure that the title of each gRPC Gateway is different
        :param msg_to_dict: protobuf.json_format.msg_to_dict func
        :param parse_dict: protobuf.json_format.parse_dict func
        :param pait: instance of pait
        :param make_response: The method of converting Message to Response object
        :param add_multi_simple_route: A function that registers multiple routes with the app
        :param kwargs: Extended parameters supported by the `add multi simple route` function of different frameworks
        """
        if title in _grpc_gateway_title_set:
            raise ValueError(f"grpc gateway title: {title} already exists")
        _grpc_gateway_title_set.add(title)

        self.app: Any = app
        self.prefix: str = prefix
        self.title: str = title
        self._parse_msg_desc: Optional[str] = parse_msg_desc
        self.msg_to_dict: Callable = msg_to_dict
        self.parse_dict: Optional[Callable] = parse_dict
        # If empty, try to get an available Pait
        self._pait: Pait = pait or getattr(self, "pait", None) or import_func_from_app("pait", app=app)  # type: ignore
        self._add_multi_simple_route = (
            add_multi_simple_route
            or getattr(self, "add_multi_simple_route", None)
            or import_func_from_app("add_multi_simple_route", app=app)
        )  # type: ignore
        self.make_response: Callable = make_response or self._make_response
        self._tag_dict: Dict[str, Tag] = {}

        # First use inspect to get the function signature of add_multi_simple_route,
        # and then generate a dictionary containing the function signature of add_multi_simple_route through kwargs
        self._add_multi_simple_route_kwargs = {
            k: kwargs[k] for k in inspect.signature(self._add_multi_simple_route).parameters.keys() if k in kwargs
        }

    def get_msg_from_dict(self, msg: Type[MessageT], request_dict: dict) -> MessageT:
        """Convert the Json data to the corresponding grpc Message object"""
        if self.parse_dict:
            request_msg: MessageT = self.parse_dict(request_dict, msg())
        else:
            request_msg = msg(**request_dict)  # type: ignore
        return request_msg

    def msg_from_dict_handle(self, msg: Type[MessageT], request_dict: dict, nested: Optional[list] = None) -> MessageT:
        """Http Request Dict to gRPC request protobuf Message
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

                If you want to convert request dict to message object, you need to specify nested=["a", "b"]

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
        gRPC response protobuf Message to HTTP response dict
            e.g.1:
                message = {
                    "a": 1,
                    "b": 2,
                    "c": 3
                } and exclude = ["a", "b"]

                return value is {"c": 3}

            e.g.2:
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
        message_dict = self.msg_to_dict(message)
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
        """reload grpc channel"""
        old_channel: Union[grpc.Channel, grpc.aio.Channel, None] = getattr(self, "channel", None)
        self.channel = channel
        # If it is grpc.aio.Channel, it will return the corresponding grpc.Channel first,
        # and then close it asynchronously
        if old_channel and auto_close:
            old_channel.close()
        return old_channel

    def init_channel(self, channel: Union[grpc.Channel, grpc.aio.Channel]) -> None:
        self.reinit_channel(channel, auto_close=True)
