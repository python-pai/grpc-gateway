"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import example_proto.book.manager_pb2
import google.protobuf.empty_pb2
import grpc

class BookManagerStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    create_book: grpc.UnaryUnaryMultiCallable[
        example_proto.book.manager_pb2.CreateBookRequest,
        google.protobuf.empty_pb2.Empty]

    delete_book: grpc.UnaryUnaryMultiCallable[
        example_proto.book.manager_pb2.DeleteBookRequest,
        google.protobuf.empty_pb2.Empty]

    get_book: grpc.UnaryUnaryMultiCallable[
        example_proto.book.manager_pb2.GetBookRequest,
        example_proto.book.manager_pb2.GetBookResult]
    """pait: {"url": "/book/get", "request_message": {"exclude_column_name": "not_use_field1,not_use_field2"}}"""

    get_book_list: grpc.UnaryUnaryMultiCallable[
        example_proto.book.manager_pb2.GetBookListRequest,
        example_proto.book.manager_pb2.GetBookListResult]
    """pait: {"url": "/book/get-list", "response_message": {"nested": "/result"}}"""


class BookManagerServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_book(self,
        request: example_proto.book.manager_pb2.CreateBookRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def delete_book(self,
        request: example_proto.book.manager_pb2.DeleteBookRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def get_book(self,
        request: example_proto.book.manager_pb2.GetBookRequest,
        context: grpc.ServicerContext,
    ) -> example_proto.book.manager_pb2.GetBookResult:
        """pait: {"url": "/book/get", "request_message": {"exclude_column_name": "not_use_field1,not_use_field2"}}"""
        pass

    @abc.abstractmethod
    def get_book_list(self,
        request: example_proto.book.manager_pb2.GetBookListRequest,
        context: grpc.ServicerContext,
    ) -> example_proto.book.manager_pb2.GetBookListResult:
        """pait: {"url": "/book/get-list", "response_message": {"nested": "/result"}}"""
        pass


def add_BookManagerServicer_to_server(servicer: BookManagerServicer, server: grpc.Server) -> None: ...
