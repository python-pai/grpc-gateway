# This is an automatically generated file, please do not change
# gen by grpc-gateway[0.0.0](https://github.com/python-pai/grpc-gateway)
from . import other_p2p
from . import other_pb2
from . import other_pb2_grpc
from ..user import user_pb2
from ..user import user_pb2_grpc
from .other_p2p import NestedMessage as NestedMessageNestedDemoRoute
from google.protobuf.empty_pb2 import Empty  # type: ignore
from grpc_gateway.protobuf_plugin.gateway import BaseStaticGrpcGatewayRoute
from grpc_gateway.rebuild_message import rebuild_message_type
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


NestedMessageNestedDemoRoute = rebuild_message_type(  # type: ignore[misc]
    NestedMessageNestedDemoRoute,
    "nested_demo_route",
    exclude_column_name=[],
    nested=["map_demo", "${}", "repeated_demo", "$[]", "$.map_demo", "${}", "repeated_demo"],
)


class OtherSocialByOptionNestedMessageJsonResponseModel(JsonResponseModel):
    class CustomerJsonResponseRespModel(BaseModel):
        code: int = Field(0, description="api code")
        msg: str = Field("success", description="api status msg")
        data: NestedMessageNestedDemoRoute = Field(description="api response data")

    name: str = "other_social_by_option_NestedMessageNestedDemoRoute"
    description: str = (
        NestedMessageNestedDemoRoute.__doc__ or ""
        if NestedMessageNestedDemoRoute.__module__ != "builtins" else ""
    )
    response_data: Type[BaseModel] = CustomerJsonResponseRespModel


async def async_nested_demo_route(
    token: str = Header.i(description="User Token"),
    req_id: str = Header.i(alias="X-Request-Id", default_factory=lambda: str(uuid4())),
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/other/other.proto_gateway"
    )
    stub: other_pb2_grpc.OtherStub = gateway.Other_stub
    request_msg: Empty = Empty()

    gateway.check_event_loop(stub.nested_demo)
    # check token
    result: user_pb2.GetUidByTokenResult = await user_pb2_grpc.UserStub(gateway.channel).get_uid_by_token(
        user_pb2.GetUidByTokenRequest(token=token)
    )
    if not result.uid:
        raise RuntimeError("Not found user by token:" + token)
    grpc_msg: other_pb2.NestedMessage = await stub.nested_demo(
        request_msg, metadata=[("req_id", req_id)]
    )
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        ["map_demo", "${}", "repeated_demo", "$[]", "$.map_demo", "${}", "repeated_demo"]
    )


def nested_demo_route(
    token: str = Header.i(description="User Token"),
    req_id: str = Header.i(alias="X-Request-Id", default_factory=lambda: str(uuid4())),
) -> Any:
    gateway: "StaticGrpcGatewayRoute" = pait_context.get().app_helper.get_attributes(
        "gateway_attr_example/grpc_proto/example_proto_by_option/other/other.proto_gateway"
    )
    stub: other_pb2_grpc.OtherStub = gateway.Other_stub
    request_msg: Empty = Empty()

    # check token
    result: user_pb2.GetUidByTokenResult = user_pb2_grpc.UserStub(gateway.channel).get_uid_by_token(
        user_pb2.GetUidByTokenRequest(token=token)
    )
    if not result.uid:
        raise RuntimeError("Not found user by token:" + token)
    grpc_msg: other_pb2.NestedMessage = stub.nested_demo(request_msg, metadata=[("req_id", req_id)])
    return gateway.msg_to_dict_handle(
        grpc_msg,
        [],
        ["map_demo", "${}", "repeated_demo", "$[]", "$.map_demo", "${}", "repeated_demo"]
    )


class StaticGrpcGatewayRoute(BaseStaticGrpcGatewayRoute):
    Other_stub: other_pb2_grpc.OtherStub
    stub_str_list: List[str] = ["Other_stub"]

    def gen_route(self) -> None:
        set_app_attribute(self.app, "gateway_attr_example/grpc_proto/example_proto_by_option/other/other.proto_gateway", self)
        # The response model generated based on Protocol is important and needs to be put first
        response_model_list: List[Type[BaseResponseModel]] = self._pait.response_model_list or []
        nested_demo_route_pait: Pait = self._pait.create_sub_pait(
            append_author=None,
            name=None,
            group=None,
            append_tag=(Tag("grpc-other_social_by_option-Other", ""), self._grpc_tag,),
            desc=None,
            summary=None,
            default_field_class=field.Json,
            response_model_list=[OtherSocialByOptionNestedMessageJsonResponseModel] + response_model_list,
        )
        pait_async_nested_demo_route = nested_demo_route_pait(feature_code="0")(async_nested_demo_route)
        pait_nested_demo_route = nested_demo_route_pait(feature_code="0")(nested_demo_route)
        self._add_multi_simple_route(
            self.app,
            SimpleRoute(
                url="/other/nested-demo",
                methods=["POST"],
                route=pait_async_nested_demo_route if self.is_async else pait_nested_demo_route
            ),
            prefix=self.config.prefix,
            title=self.config.title,
            **self._add_multi_simple_route_kwargs
        )
