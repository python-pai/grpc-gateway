"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import example.grpc_proto.example_proto_by_option.book.social_pb2
import google.protobuf.empty_pb2
import grpc

class BookSocialStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    like_book: grpc.UnaryUnaryMultiCallable[
        example.grpc_proto.example_proto_by_option.book.social_pb2.LikeBookRequest,
        google.protobuf.empty_pb2.Empty]

    like_multi_book: grpc.UnaryUnaryMultiCallable[
        example.grpc_proto.example_proto_by_option.book.social_pb2.LikeBookMapRequest,
        google.protobuf.empty_pb2.Empty]

    get_book_like: grpc.UnaryUnaryMultiCallable[
        example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookLikesRequest,
        example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookLikesListResult]

    get_book_like_other: grpc.UnaryUnaryMultiCallable[
        example.grpc_proto.example_proto_by_option.book.social_pb2.NestedGetBookLikesRequest,
        example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookLikesListResult]

    comment_book: grpc.UnaryUnaryMultiCallable[
        example.grpc_proto.example_proto_by_option.book.social_pb2.CommentBookRequest,
        google.protobuf.empty_pb2.Empty]

    get_book_comment: grpc.UnaryUnaryMultiCallable[
        example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookCommentRequest,
        example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookCommentListResult]


class BookSocialServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def like_book(self,
        request: example.grpc_proto.example_proto_by_option.book.social_pb2.LikeBookRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def like_multi_book(self,
        request: example.grpc_proto.example_proto_by_option.book.social_pb2.LikeBookMapRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def get_book_like(self,
        request: example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookLikesRequest,
        context: grpc.ServicerContext,
    ) -> example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookLikesListResult: ...

    @abc.abstractmethod
    def get_book_like_other(self,
        request: example.grpc_proto.example_proto_by_option.book.social_pb2.NestedGetBookLikesRequest,
        context: grpc.ServicerContext,
    ) -> example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookLikesListResult: ...

    @abc.abstractmethod
    def comment_book(self,
        request: example.grpc_proto.example_proto_by_option.book.social_pb2.CommentBookRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def get_book_comment(self,
        request: example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookCommentRequest,
        context: grpc.ServicerContext,
    ) -> example.grpc_proto.example_proto_by_option.book.social_pb2.GetBookCommentListResult: ...


def add_BookSocialServicer_to_server(servicer: BookSocialServicer, server: grpc.Server) -> None: ...
