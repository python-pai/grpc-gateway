import inspect
from abc import ABCMeta
from dataclasses import dataclass, field
from sys import modules
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import grpc
from google.protobuf.empty_pb2 import Empty  # type: ignore
from pait import _pydanitc_adapter
from pait.app.base.simple_route import SimpleRoute
from pait.core import Pait
from pait.field import BaseRequestResourceField, Json, Query
from pait.model.response import BaseResponseModel, JsonResponseModel
from pait.model.tag import Tag
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

from grpc_gateway.base_gateway import BaseGrpcGatewayRoute, BaseGrpcGatewayRouteConfig
from grpc_gateway.desc_template import DescTemplate
from grpc_gateway.dynamic_gateway.inspect import GrpcMethodModel, Message, ParseStub
from grpc_gateway.model import BuildMessageModel
from grpc_gateway.rebuild_message import rebuild_message_type

__all__ = ["DynamicGrpcGatewayRoute", "AsyncGrpcGatewayRoute", "GrpcGatewayRoute", "GrpcGatewayRouteConfig"]

_http_method_default_field_dict: Dict[str, Type[BaseRequestResourceField]] = {"GET": Query, "POST": Json}
GEN_RESP_MODEL_HANDLE_TYPE = Callable[[GrpcMethodModel, Any], Type[BaseResponseModel]]


def _gen_response_model_handle(grpc_model: GrpcMethodModel, response_model: Any) -> Type[BaseResponseModel]:
    class CustomerJsonResponseModel(JsonResponseModel):
        name: str = grpc_model.response.DESCRIPTOR.name
        description: str = grpc_model.response.__doc__ or ""

        response_data: Type[BaseModel] = response_model

    return CustomerJsonResponseModel


def _url_handle(url: str) -> str:
    return url.replace(".", "-")


@dataclass
class GrpcGatewayRouteConfig(BaseGrpcGatewayRouteConfig):
    # url processing function, the default symbol: `.` is converted to `-`
    url_handler: Callable[[str], str] = _url_handle
    # DescTemplate object, which can extend and modify template adaptation rules through inheritance
    desc_template: Type[DescTemplate] = DescTemplate
    # Methods for generating OpenAPI response objects
    gen_response_model_handle: GEN_RESP_MODEL_HANDLE_TYPE = _gen_response_model_handle
    http_method_default_field_dict: Dict[str, Type[BaseRequestResourceField]] = field(
        default_factory=lambda: _http_method_default_field_dict
    )
    # The prefix of the comment, the default is `grpc-gateway`
    comment_prefix: str = "grpc-gateway"
    # googl.protobuf.empty_pb2.Empty cannot be parsed by pydantic, and a type needs to be defined that can be resolved
    empty_type: Type = field(default=dict)


class DynamicGrpcGatewayRoute(BaseGrpcGatewayRoute[GrpcGatewayRouteConfig]):
    def __init__(self, app: Any, *stub_list: Any, config: Optional[GrpcGatewayRouteConfig] = None):
        """
        :param app: Instance object of the web framework
        :param stub_list: gRPC Stub List
        :param config: GrpcGatewayRoute Config
        """
        super().__init__(app=app, config=config or GrpcGatewayRouteConfig())

        self.grpc_method_url_func_dict: Dict[str, Callable] = {}
        self._gen_response_model_handle: GEN_RESP_MODEL_HANDLE_TYPE = self.config.gen_response_model_handle
        self.stub_list: Tuple[Any, ...] = stub_list
        self._add_route(app)

    def _gen_r_pydantic_class(
        self,
        grpc_model: GrpcMethodModel,
        r_message: Type[Message],
        build_model: BuildMessageModel,
    ) -> Type:
        http_method: str = grpc_model.grpc_service_option_model.http_method
        if http_method not in self.config.http_method_default_field_dict:
            raise ValueError(f"{http_method} not in http_method_default_field_dict")  # pragma: no cover
        r_model: Type[BaseModel] = msg_to_pydantic_model(
            r_message,
            default_field=self.config.http_method_default_field_dict[http_method],
            comment_prefix=self.config.comment_prefix,
            desc_template=self.config.desc_template,
            parse_msg_desc_method=getattr(r_message, "_message_module")
            if self.config.parse_msg_desc == "by_mypy"
            else self.config.parse_msg_desc,
        )
        if build_model.has_value():
            return rebuild_message_type(
                r_model,
                grpc_model.invoke_name,
                exclude_column_name=build_model.exclude_column_name,
                nested=build_model.nested,
            )
        else:
            return r_model

    def _gen_request_pydantic_class(self, grpc_model: GrpcMethodModel) -> Type:
        """
        Generate a pydantic class that automatically generates the corresponding request according to the Protocol
         Message (Field is pait.field)
        """
        return self._gen_r_pydantic_class(
            grpc_model,
            grpc_model.request,
            grpc_model.grpc_service_option_model.request_message,
        )

    def _gen_response_pydantic_class(self, grpc_model: GrpcMethodModel) -> Type:
        if grpc_model.response is Empty:
            response_model: Any = self.config.empty_type
        else:
            response_model = self._gen_r_pydantic_class(
                grpc_model,
                grpc_model.response,
                grpc_model.grpc_service_option_model.response_message,
            )

            # Rename it,
            # otherwise it will overwrite the existing scheme with the same name when generating OpenAPI documents.
            def _rename_type_handle(cls: type) -> type:
                if inspect.isclass(cls) and issubclass(cls, BaseModel):
                    cls = type(f"{grpc_model.grpc_method_url}-{cls.__name__}-RespModel", (cls,), {})
                elif hasattr(cls, "__origin__") and hasattr(cls, "__args__") and hasattr(cls, "copy_with"):
                    new_args = []
                    for item in cls.__args__:
                        new_args.append(_rename_type_handle(item))
                    cls.copy_with(tuple(new_args))
                return cls

            response_model = _rename_type_handle(response_model)

        return self._gen_response_model_handle(grpc_model, response_model)

    def _gen_pait_from_grpc_model(self, grpc_model: GrpcMethodModel) -> Pait:
        """Generate the corresponding pait instance according to the object of the grpc calling method"""
        tag_list: List[Tag] = [self._grpc_tag]
        for tag, desc in grpc_model.grpc_service_option_model.tag or [
            ("grpc" + "-" + self.config.url_handler(grpc_model.grpc_method_url.split("/")[1]), "")
        ]:
            if tag in self._tag_dict:
                pait_tag: Tag = self._tag_dict[tag]
            else:
                pait_tag = Tag(tag, desc)
                self._tag_dict[tag] = pait_tag
            tag_list.append(pait_tag)

        # The response model generated based on Protocol is important and needs to be put first
        response_model_list: List[Type[BaseResponseModel]] = [self._gen_response_pydantic_class(grpc_model)]
        if self._pait.response_model_list:
            response_model_list.extend(self._pait.response_model_list)

        return self._pait.create_sub_pait(
            append_author=grpc_model.grpc_service_option_model.author or None,
            name=grpc_model.grpc_service_option_model.name or None,
            group=grpc_model.grpc_service_option_model.group or grpc_model.grpc_method_url.split("/")[1],
            append_tag=tuple(tag_list) if tag_list else None,
            desc=grpc_model.grpc_service_option_model.desc or None,
            summary=grpc_model.grpc_service_option_model.summary or None,
            default_field_class=Query if grpc_model.grpc_service_option_model.http_method == "GET" else Json,
            response_model_list=response_model_list,
        )

    def get_grpc_func(self, grpc_model: GrpcMethodModel) -> Callable:
        """Get grpc invoke func"""
        func: Optional[Callable] = self.grpc_method_url_func_dict.get(grpc_model.grpc_method_url, None)
        if not func:
            raise RuntimeError(  # pragma: no cover
                f"{grpc_model.alias_grpc_method_url}'s func is not found, "
                f"Please call {self.init_channel.__name__} to register the channel"
            )
        return func

    def gen_route(self, grpc_model: GrpcMethodModel, request_pydantic_model_class: Type) -> Callable:
        """Generate the routing function corresponding to grpc invoke fun"""
        raise NotImplementedError()

    def _gen_route_func(self, grpc_model: GrpcMethodModel) -> Optional[Callable]:
        if grpc_model.grpc_service_option_model.enable is False:
            return None

        request_pydantic_model_class: Type = self._gen_request_pydantic_class(grpc_model)
        pait: Pait = self._gen_pait_from_grpc_model(grpc_model)
        _route = self.gen_route(grpc_model, request_pydantic_model_class)
        # change route func name and qualname
        _route.__name__ = (
            (self.config.title + "." + grpc_model.alias_grpc_method_url).replace(".", "_").replace(" ", "_")
        )
        _route.__qualname__ = _route.__qualname__.replace("._route", "." + _route.__name__)
        modules_dict = modules[_route.__module__].__dict__
        if "request_pydantic_model_class" in modules_dict:
            raise KeyError("request_pydantic_model_class already exists")
        # Since the route is generated dynamically, pait will not be able to resolve the type of
        # 'request_pydantic_model_class', so it needs to inject 'request_pydantic_model_class' into the module
        # where the route is generated
        modules_dict["request_pydantic_model_class"] = request_pydantic_model_class
        _route = pait(feature_code=grpc_model.grpc_method_url)(_route)
        # After parsing the request, remove the request pydantic model class to prevent bugs
        modules_dict.pop("request_pydantic_model_class")
        return _route

    def _add_route(self, app: Any) -> Any:  # type: ignore
        """Add the generated routing function to the corresponding web framework instance"""
        for stub_class in self.stub_list:
            parse_stub: ParseStub = ParseStub(stub_class, comment_prefix=self.config.comment_prefix)
            simple_route_list: List[SimpleRoute] = []
            for _, grpc_model_list in parse_stub.method_list_dict.items():
                for grpc_model in grpc_model_list:
                    _route = self._gen_route_func(grpc_model)
                    if not _route:
                        continue
                    simple_route_list.append(
                        SimpleRoute(
                            url=self.config.url_handler(grpc_model.grpc_service_option_model.url),
                            route=_route,
                            methods=[grpc_model.grpc_service_option_model.http_method],
                        )
                    )
            self._add_multi_simple_route(
                app,
                *simple_route_list,
                prefix=self.config.prefix,
                title=self.config.title + parse_stub.name,
                **self._add_multi_simple_route_kwargs,
            )

    def reinit_channel(
        self, channel: Union[grpc.Channel, grpc.aio.Channel], auto_close: bool = False
    ) -> Union[grpc.Channel, grpc.aio.Channel, None]:
        for stub_class in self.stub_list:
            stub = stub_class(channel)
            for func in stub.__dict__.values():
                grpc_method_url = func._method  # type: ignore
                if isinstance(grpc_method_url, bytes):
                    grpc_method_url = grpc_method_url.decode()
                self.grpc_method_url_func_dict[grpc_method_url] = func
        return super().reinit_channel(channel, auto_close)


class GrpcGatewayRoute(DynamicGrpcGatewayRoute, metaclass=ABCMeta):
    def gen_route(self, grpc_model: GrpcMethodModel, request_pydantic_model_class: Type[BaseModel]) -> Callable:
        def _route(request_pydantic_model: request_pydantic_model_class) -> Any:  # type: ignore
            func: Callable = self.get_grpc_func(grpc_model)
            request_msg: Message = self.msg_from_dict_handle(
                grpc_model.request,
                _pydanitc_adapter.model_dump(request_pydantic_model),
                grpc_model.grpc_service_option_model.request_message.nested,
            )

            grpc_msg: Message = func(request_msg)
            return self.msg_to_dict_handle(
                grpc_msg,
                grpc_model.grpc_service_option_model.response_message.exclude_column_name,
                grpc_model.grpc_service_option_model.response_message.nested,
            )

        return _route

    def reinit_channel(self, channel: grpc.Channel, auto_close: bool = False) -> Union[grpc.Channel, None]:
        return super().reinit_channel(channel, auto_close)


class AsyncGrpcGatewayRoute(DynamicGrpcGatewayRoute, metaclass=ABCMeta):
    def get_grpc_func(self, grpc_model: GrpcMethodModel) -> Callable:
        func = super().get_grpc_func(grpc_model)
        self.check_event_loop(func)
        return func

    def gen_route(self, grpc_model: GrpcMethodModel, request_pydantic_model_class: Type[BaseModel]) -> Callable:
        async def _route(request_pydantic_model: request_pydantic_model_class) -> Any:  # type: ignore
            func: Callable = self.get_grpc_func(grpc_model)
            request_msg: Message = self.msg_from_dict_handle(
                grpc_model.request,
                _pydanitc_adapter.model_dump(request_pydantic_model),
                grpc_model.grpc_service_option_model.request_message.nested,
            )
            grpc_msg: Message = await func(request_msg)
            return self.msg_to_dict_handle(
                grpc_msg,
                grpc_model.grpc_service_option_model.response_message.exclude_column_name,
                grpc_model.grpc_service_option_model.response_message.nested,
            )

        return _route

    def init_channel(self, channel: grpc.aio.Channel) -> None:
        super().init_channel(channel)

    def reinit_channel(self, channel: grpc.aio.Channel, auto_close: bool = False) -> Union[grpc.aio.Channel, None]:
        return super().reinit_channel(channel, auto_close)
