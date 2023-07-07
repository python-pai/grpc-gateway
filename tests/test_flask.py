from contextlib import contextmanager
from typing import Generator

import pytest
from flask import Flask
from flask.ctx import AppContext
from flask.testing import FlaskClient
from pait.app.flask import TestHelper as _TestHelper

from example.flask_example import grpc_route
from example.flask_example.utils import api_exception
from grpc_gateway.gateway.base_gateway import _grpc_gateway_title_set
from grpc_gateway.gateway.dynamic_gateway import GrpcGatewayRoute
from tests.base_api_test import BaseTest
from tests.conftest import grpc_request_test, grpc_test_openapi


@contextmanager
def client_ctx() -> Generator[FlaskClient, None, None]:
    _grpc_gateway_title_set.clear()
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    app: Flask = Flask("test")
    app.errorhandler(Exception)(api_exception)
    client: FlaskClient = app.test_client()
    # Establish an application context before running the tests.
    ctx: AppContext = app.app_context()
    ctx.push()
    yield client  # this is where the testing happens!
    ctx.pop()


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    with client_ctx() as client:
        yield client


@contextmanager
def base_test_ctx() -> Generator[BaseTest, None, None]:
    with client_ctx() as client:
        yield BaseTest(client, _TestHelper)


class TestFlaskGrpc:
    def test_create_user(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import CreateUserRequest

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in ("/api/user/create", "/api/static/user/create"):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(
                        url,
                        json={"uid": "10086", "user_name": "so1n", "pw": "123456", "sex": 0},
                    ).data
                    assert body == b'{"code":0,"data":{},"msg":""}\n'
                    message: CreateUserRequest = queue.get(timeout=1)
                    assert message.uid == "10086"
                    assert message.user_name == "so1n"
                    assert message.password == "123456"
                    assert message.sex == 0

    def test_get_book(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookRequest

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in (
                "/api/book/get",
                "/api/static/book/get",
            ):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(url + "?isbn=xxxa", headers={"token": "token"}).data
                    assert body == (
                        b'{"code":0,'
                        b'"data":{"book_author":"","book_desc":"","book_name":"","book_url":"","isbn":""},"msg":""}\n'
                    )
                    queue.get(timeout=1)
                    message: GetBookRequest = queue.get(timeout=1)
                    assert message.isbn == "xxxa"

    def test_get_book_list(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookListRequest

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in (
                "/api/book/get-list",
                "/api/static/book/get-list",
            ):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(
                        url, json={"limit": 0, "next_create_time": "2023-04-10 18:44:36"}, headers={"token": "token"}
                    ).data
                    assert body == (b'{"code":0,"data":[],"msg":""}\n')
                    queue.get(timeout=1)
                    message: GetBookListRequest = queue.get(timeout=1)
                    assert message.limit == 0

    def test_get_book_like(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.social_pb2 import (
            GetBookLikesRequest,
            NestedGetBookLikesRequest,
        )

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in (
                "/api/book/get-book-like",
                "/api/book/get-book-like-other",
                "/api/static/book/get-book-like",
                "/api/static/book/get-book-like-other",
            ):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(url, json={"isbn": ["xxxa", "xxxb"]}, headers={"token": "token"}).data
                    assert body == b'{"code":0,"data":{"result":[]},"msg":""}\n'
                    queue.get(timeout=1)
                    if not url.endswith("other"):
                        message1: GetBookLikesRequest = queue.get(timeout=1)
                        assert message1.isbn == ["xxxa", "xxxb"]
                    else:
                        message2: NestedGetBookLikesRequest = queue.get(timeout=1)
                        assert message2.nested.isbn == ["xxxa", "xxxb"]

    def test_login(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import LoginUserRequest

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in ("/api/user/login", "/api/static/user/login"):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(url, json={"uid": "10086", "password": "pw"}).data
                    assert body == b'{"code":0,"data":{"token":"","uid":"","user_name":""},"msg":""}\n'
                    message: LoginUserRequest = queue.get(timeout=1)
                    assert message.uid == "10086"
                    assert message.password == "pw"

    def test_logout(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import LogoutUserRequest

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in ("/api/user/logout", "/api/static/user/logout"):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(url, json={"uid": "10086"}, headers={"token": "token"}).data
                    assert body == b'{"code":0,"data":{},"msg":""}\n'
                    message: LogoutUserRequest = queue.get(timeout=1)
                    assert message.uid == "10086"
                    assert message.token == "token"

    def test_delete_fail_token(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import GetUidByTokenRequest

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in ("/api/user/delete", "/api/static/user/delete"):
                with grpc_request_test(client.application) as queue:
                    body: bytes = client.post(
                        url,
                        json={"uid": "10086"},
                        headers={"token": "fail_token"},
                    ).data
                    assert body == b'{"code":-1,"msg":"Not found user by token:fail_token"}\n'
                    message: GetUidByTokenRequest = queue.get(timeout=1)
                    assert message.token == "fail_token"

    def test_nested_demo(self) -> None:
        pass

        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            for url in ("/api/other/nested-demo", "/api/static/other/nested-demo"):
                with grpc_request_test(client.application):
                    body: bytes = client.post(url, headers={"token": "token"}).data
                    assert body == b'{"code":0,"data":{"a":[{"map_demo":{"c":[{"a":1,"b":"foo"}]}}]},"msg":""}\n'

    def test_grpc_openapi(self) -> None:
        with client_ctx() as client:
            grpc_route.add_grpc_gateway_route(client.application)

            grpc_test_openapi(client.application)
            grpc_test_openapi(client.application, url_prefix="/api/static", option_str="_by_option")

    def test_grpc_openapi_by_protobuf_file(self) -> None:
        with base_test_ctx() as base_test:
            base_test.grpc_openapi_by_protobuf_file(base_test.client.application, GrpcGatewayRoute)

    def test_grpc_openapi_by_option(self) -> None:
        with base_test_ctx() as base_test:
            base_test.grpc_openapi_by_option(base_test.client.application, GrpcGatewayRoute)
