# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from example.grpc_common.python_example_proto_code.example_proto.other import other_pb2 as example__proto_dot_other_dot_other__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class OtherStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.nested_demo = channel.unary_unary(
                '/other_social.Other/nested_demo',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=example__proto_dot_other_dot_other__pb2.NestedMessage.FromString,
                )


class OtherServicer(object):
    """Missing associated documentation comment in .proto file."""

    def nested_demo(self, request, context):
        """grpc-gateway: {"http_method": "POST", "url": "/other/nested-demo"}
        grpc-gateway: {"response_message": {"nested": "/map_demo/${}/repeated_demo/$[]/$.map_demo/${}/repeated_demo"}}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OtherServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'nested_demo': grpc.unary_unary_rpc_method_handler(
                    servicer.nested_demo,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=example__proto_dot_other_dot_other__pb2.NestedMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'other_social.Other', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Other(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def nested_demo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/other_social.Other/nested_demo',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            example__proto_dot_other_dot_other__pb2.NestedMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
