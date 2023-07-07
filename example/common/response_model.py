from typing import Any, Type

from any_api.openapi import BaseResponseModel
from google.protobuf.empty_pb2 import Empty  # type: ignore
from pait.model import JsonResponseModel
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel, Field

from grpc_gateway.inspect import GrpcMethodModel
from grpc_gateway.rebuild_message import rebuild_message_type


def gen_response_model_handle(grpc_model: GrpcMethodModel) -> Type[BaseResponseModel]:
    if grpc_model.response is Empty:
        response_model: Any = dict
    elif grpc_model.grpc_service_option_model.response_message:
        response_model = rebuild_message_type(
            msg_to_pydantic_model(grpc_model.response),
            grpc_model.invoke_name,
            exclude_column_name=grpc_model.grpc_service_option_model.response_message.exclude_column_name,
            nested=grpc_model.grpc_service_option_model.response_message.nested,
        )
    else:
        response_model = msg_to_pydantic_model(grpc_model.response)

    class CustomerJsonResponseModel(JsonResponseModel):
        class CustomerJsonResponseRespModel(BaseModel):
            code: int = Field(0, description="api code")
            msg: str = Field("success", description="api status msg")
            data: response_model = Field(description="api response data")  # type: ignore

        name: str = grpc_model.response.DESCRIPTOR.name
        response_data: Type[BaseModel] = CustomerJsonResponseRespModel

    return CustomerJsonResponseModel
