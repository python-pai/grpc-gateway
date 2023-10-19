from google.protobuf.empty_pb2 import Empty  # type: ignore
from pydantic import BaseModel

from example.grpc_common.python_example_proto_code.example_proto_by_option.user import user_pb2
from grpc_gateway.dynamic_gateway.gateway import _gen_response_model_handle
from grpc_gateway.dynamic_gateway.inspect import GrpcMethodModel
from grpc_gateway.model import GrpcServiceOptionModel
from grpc_gateway.protobuf_types import Message


class TestUtil:
    def test_gen_response_model_handle(self) -> None:
        # invoke_name: str
        # grpc_method_url: str
        # alias_grpc_method_url: str
        # grpc_service_option_model: GrpcServiceOptionModel
        # # func: Callable
        # request: Type[Message] = Message
        # response: Type[Message] = Message
        assert issubclass(
            _gen_response_model_handle(
                GrpcMethodModel(
                    invoke_name="",
                    grpc_method_url="",
                    alias_grpc_method_url="",
                    request=Message,
                    response=Empty,
                    grpc_service_option_model=GrpcServiceOptionModel(),
                )
            ).response_data,
            dict,
        )
        assert issubclass(
            _gen_response_model_handle(
                GrpcMethodModel(
                    invoke_name="",
                    grpc_method_url="",
                    alias_grpc_method_url="",
                    request=Message,
                    response=user_pb2.GetUidByTokenResult,
                    grpc_service_option_model=GrpcServiceOptionModel(),
                )
            ).response_data,
            BaseModel,
        )
