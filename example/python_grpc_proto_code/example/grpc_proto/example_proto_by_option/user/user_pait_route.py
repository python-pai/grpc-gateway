# This is an automatically generated file, please do not change
# gen by grpc-gateway[0.0.0](https://github.com/python-pai/grpc-gateway)
from . import user_p2p
from . import user_pb2
from . import user_pb2_grpc
from ..user import user_pb2
from ..user import user_pb2_grpc
from google.protobuf.empty_pb2 import Empty  # type: ignore
from grpc_gateway.protobuf_plugin.gateway import BaseStaticGrpcGatewayRoute
from pait import field
from pait.app.any import SimpleRoute
from pait.app.any import set_app_attribute
from pait.core import Pait
from pait.field import Header
from pait.g import pait_context
from pait.model.response import BaseResponseModel
from pait.model.response import JsonResponseModel
from pait.model.tag import Tag
from pydantic import BaseModel
from pydantic import Field
from typing import Any
from typing import Callable
from typing import List
from typing import Type
from uuid import uuid4


class UserByOptionEmptyJsonResponseModel(JsonResponseModel):
    class CustomerJsonResponseRespModel(BaseModel):
        code: int = Field(0, description="api code")
        msg: str = Field("success", description="api status msg")
        data: dict = Field(description="api response data")

    name: str = "user_by_option_Empty"
    description: str = (
        dict.__doc__ or ""
        if dict.__module__ != "builtins" else ""
    )
    response_data: Type[BaseModel] = CustomerJsonResponseRespModel


class UserByOptionLoginUserResultJsonResponseModel(JsonResponseModel):
    class CustomerJsonResponseRespModel(BaseModel):
        code: int = Field(0, description="api code")
        msg: str = Field("success", description="api status msg")
        data: user_p2p.LoginUserResult = Field(description="api response data")

    name: str = "user_by_option_user_p2p.LoginUserResult"
    description: str = (
        user_p2p.LoginUserResult.__doc__ or ""
        if user_p2p.LoginUserResult.__module__ != "builtins" else ""
    )
    response_data: Type[BaseModel] = CustomerJsonResponseRespModel


async def async_logout_user_route(
    request_pydantic_model: user_p2p.LogoutUserRequest,
    token: str = Header.i(description="User Token"),
    req_id: str = Header.i(alias="X-Request-Id", default_factory=lambda: str(uuid4())),
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    request_dict: dict = request_pydantic_model.model_dump()
    request_dict["token"] = token
    request_msg: user_pb2.LogoutUserRequest = gateway.msg_from_dict_handle(
        user_pb2.LogoutUserRequest,
        request_dict,
        []
    )
    gateway.check_event_loop(gateway.User_stub.logout_user)
    grpc_msg: Empty = await gateway.User_stub.logout_user(
        request_msg, metadata=[("req_id", req_id)])
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


def logout_user_route(
    request_pydantic_model: user_p2p.LogoutUserRequest,
    token: str = Header.i(description="User Token"),
    req_id: str = Header.i(alias="X-Request-Id", default_factory=lambda: str(uuid4())),
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    request_dict: dict = request_pydantic_model.model_dump()
    request_dict["token"] = token
    request_msg: user_pb2.LogoutUserRequest = gateway.msg_from_dict_handle(
        user_pb2.LogoutUserRequest,
        request_dict,
        []
    )
    grpc_msg: Empty = gateway.User_stub.logout_user(
        request_msg, metadata=[("req_id", req_id)])
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


async def async_login_user_route(
    request_pydantic_model: user_p2p.LoginUserRequest
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    request_msg: user_pb2.LoginUserRequest = gateway.msg_from_dict_handle(
        user_pb2.LoginUserRequest,
        request_pydantic_model.model_dump(),
        []
    )
    gateway.check_event_loop(gateway.User_stub.login_user)
    grpc_msg: user_pb2.LoginUserResult = await gateway.User_stub.login_user(
        request_msg
    )
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


def login_user_route(
    request_pydantic_model: user_p2p.LoginUserRequest
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    request_msg: user_pb2.LoginUserRequest = gateway.msg_from_dict_handle(
        user_pb2.LoginUserRequest,
        request_pydantic_model.model_dump(),
        []
    )
    grpc_msg: user_pb2.LoginUserResult = gateway.User_stub.login_user(request_msg)
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


async def async_create_user_route(
    request_pydantic_model: user_p2p.CreateUserRequest
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    request_msg: user_pb2.CreateUserRequest = gateway.msg_from_dict_handle(
        user_pb2.CreateUserRequest,
        request_pydantic_model.model_dump(),
        []
    )
    gateway.check_event_loop(gateway.User_stub.create_user)
    grpc_msg: Empty = await gateway.User_stub.create_user(
        request_msg
    )
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


def create_user_route(
    request_pydantic_model: user_p2p.CreateUserRequest
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    request_msg: user_pb2.CreateUserRequest = gateway.msg_from_dict_handle(
        user_pb2.CreateUserRequest,
        request_pydantic_model.model_dump(),
        []
    )
    grpc_msg: Empty = gateway.User_stub.create_user(request_msg)
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


async def async_delete_user_route(
    request_pydantic_model: user_p2p.DeleteUserRequest,
    token: str = Header.i(description="User Token"),
    req_id: str = Header.i(alias="X-Request-Id", default_factory=lambda: str(uuid4())),
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    stub: user_pb2_grpc.UserStub = gateway.User_stub
    request_msg: user_pb2.DeleteUserRequest = gateway.msg_from_dict_handle(
        user_pb2.DeleteUserRequest,
        request_pydantic_model.model_dump(),
        []
    )

    gateway.check_event_loop(stub.delete_user)
    # check token
    result: user_pb2.GetUidByTokenResult = await user_pb2_grpc.UserStub(gateway.channel).get_uid_by_token(
        user_pb2.GetUidByTokenRequest(token=token)
    )
    if not result.uid:
        raise RuntimeError("Not found user by token:" + token)
    grpc_msg: Empty = await stub.delete_user(
        request_msg, metadata=[("req_id", req_id)]
    )
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


def delete_user_route(
    request_pydantic_model: user_p2p.DeleteUserRequest,
    token: str = Header.i(description="User Token"),
    req_id: str = Header.i(alias="X-Request-Id", default_factory=lambda: str(uuid4())),
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway"
    )
    stub: user_pb2_grpc.UserStub = gateway.User_stub
    request_msg: user_pb2.DeleteUserRequest = gateway.msg_from_dict_handle(
        user_pb2.DeleteUserRequest,
        request_pydantic_model.model_dump(),
        []
    )

    # check token
    result: user_pb2.GetUidByTokenResult = user_pb2_grpc.UserStub(gateway.channel).get_uid_by_token(
        user_pb2.GetUidByTokenRequest(token=token)
    )
    if not result.uid:
        raise RuntimeError("Not found user by token:" + token)
    grpc_msg: Empty = stub.delete_user(request_msg, metadata=[("req_id", req_id)])
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        []
    )


class StaticGrpcGatewayRoute(BaseStaticGrpcGatewayRoute):
    User_stub: user_pb2_grpc.UserStub
    stub_str_list: List[str] = ["User_stub"]

    def gen_route(self) -> None:
        set_app_attribute(self.app, "gateway_attr_example/grpc_proto/example_proto_by_option/user/user.proto_gateway", self)
        # The response model generated based on Protocol is important and needs to be put first
        response_model_list: List[Type[BaseResponseModel]] = self._pait.response_model_list or []
        logout_user_route_pait: Pait = self._pait.create_sub_pait(
            append_author=None,
            name=None,
            group=None,
            append_tag=(Tag("grpc-user", "grpc_user_service"), Tag("grpc-user_by_option-User", ""), self._grpc_tag,),
            desc=None,
            summary="User exit from the system",
            default_field_class=field.Json,
            response_model_list=[UserByOptionEmptyJsonResponseModel] + response_model_list,
        )
        pait_async_logout_user_route = logout_user_route_pait(feature_code="0")(async_logout_user_route)
        pait_logout_user_route = logout_user_route_pait(feature_code="0")(logout_user_route)
        login_user_route_pait: Pait = self._pait.create_sub_pait(
            append_author=None,
            name=None,
            group=None,
            append_tag=(Tag("grpc-user", "grpc_user_service"), Tag("grpc-user_by_option-User", ""), self._grpc_tag,),
            desc=None,
            summary="User login to system",
            default_field_class=field.Json,
            response_model_list=[UserByOptionLoginUserResultJsonResponseModel] + response_model_list,
        )
        pait_async_login_user_route = login_user_route_pait(feature_code="0")(async_login_user_route)
        pait_login_user_route = login_user_route_pait(feature_code="0")(login_user_route)
        create_user_route_pait: Pait = self._pait.create_sub_pait(
            append_author=None,
            name=None,
            group=None,
            append_tag=(Tag("grpc-user", "grpc_user_service"), Tag("grpc-user-system", "grpc_user_service"), Tag("grpc-user_by_option-User", ""), self._grpc_tag,),
            desc=None,
            summary="Create users through the system",
            default_field_class=field.Json,
            response_model_list=[UserByOptionEmptyJsonResponseModel] + response_model_list,
        )
        pait_async_create_user_route = create_user_route_pait(feature_code="0")(async_create_user_route)
        pait_create_user_route = create_user_route_pait(feature_code="0")(create_user_route)
        delete_user_route_pait: Pait = self._pait.create_sub_pait(
            append_author=None,
            name=None,
            group=None,
            append_tag=(Tag("grpc-user", "grpc_user_service"), Tag("grpc-user-system", "grpc_user_service"), Tag("grpc-user_by_option-User", ""), self._grpc_tag,),
            desc="This interface performs a logical delete, not a physical delete",
            summary=None,
            default_field_class=field.Json,
            response_model_list=[UserByOptionEmptyJsonResponseModel] + response_model_list,
        )
        pait_async_delete_user_route = delete_user_route_pait(feature_code="0")(async_delete_user_route)
        pait_delete_user_route = delete_user_route_pait(feature_code="0")(delete_user_route)
        self._add_multi_simple_route(
            self.app,
            SimpleRoute(
                url="/user/logout",
                methods=["POST"],
                route=pait_async_logout_user_route if self.is_async else pait_logout_user_route
            ),
            SimpleRoute(
                url="/user/login",
                methods=["POST"],
                route=pait_async_login_user_route if self.is_async else pait_login_user_route
            ),
            SimpleRoute(
                url="/user/create",
                methods=["POST"],
                route=pait_async_create_user_route if self.is_async else pait_create_user_route
            ),
            SimpleRoute(
                url="/user/delete",
                methods=["POST"],
                route=pait_async_delete_user_route if self.is_async else pait_delete_user_route
            ),
            prefix=self.config.prefix,
            title=self.config.title,
            **self._add_multi_simple_route_kwargs
        )
