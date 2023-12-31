"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import example.grpc_proto.example_proto_by_option.other.other_pb2
import google.protobuf.empty_pb2
import grpc

class OtherStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    nested_demo: grpc.UnaryUnaryMultiCallable[
        google.protobuf.empty_pb2.Empty,
        example.grpc_proto.example_proto_by_option.other.other_pb2.NestedMessage]


class OtherServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def nested_demo(self,
        request: google.protobuf.empty_pb2.Empty,
        context: grpc.ServicerContext,
    ) -> example.grpc_proto.example_proto_by_option.other.other_pb2.NestedMessage: ...


def add_OtherServicer_to_server(servicer: OtherServicer, server: grpc.Server) -> None: ...
