from typing import Any, Type

from any_api.openapi import BaseResponseModel
from google.protobuf.empty_pb2 import Empty  # type: ignore
from pait.model.response import JsonResponseModel
from pydantic import BaseModel, Field

from grpc_gateway.dynamic_gateway.inspect import GrpcMethodModel


def gen_response_model_handle(grpc_model: GrpcMethodModel, response_model: Any) -> Type[BaseResponseModel]:
    class CustomerJsonResponseModel(JsonResponseModel):
        class CustomerJsonResponseRespModel(BaseModel):
            code: int = Field(0, description="api code")
            msg: str = Field("success", description="api status msg")
            data: response_model = Field(description="api response data")  # type: ignore

        name: str = grpc_model.response.DESCRIPTOR.name
        response_data: Type[BaseModel] = CustomerJsonResponseRespModel

    return CustomerJsonResponseModel
