import json
import logging
from contextlib import contextmanager
from typing import Generator

import pytest
from pait.app.sanic import TestHelper as _TestHelper
from pait.exceptions import PaitBaseException
from pydantic import ValidationError
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic_testing.testing import SanicTestClient

from example.sanic_example import grpc_route
from example.sanic_example.utils import api_exception
from grpc_gateway.base_gateway import _grpc_gateway_title_set
from grpc_gateway.dynamic_gateway.gateway import AsyncGrpcGatewayRoute as GrpcGatewayRoute
from tests.base_api_test import BaseTest
from tests.conftest import grpc_request_test, grpc_test_openapi


def get_app() -> Sanic:
    logging.disable()  # don't know where to configure the log, the test environment will be canceled log
    _grpc_gateway_title_set.clear()
    app: Sanic = Sanic("test", configure_logging=False)
    app.exception(PaitBaseException, ValidationError, RuntimeError, SanicException)(api_exception)
    app.config.ACCESS_LOG = False
    return app


@contextmanager
def client_ctx() -> Generator[SanicTestClient, None, None]:
    app = get_app()
    grpc_route.add_grpc_gateway_route(app)
    yield app.test_client


@contextmanager
def base_test_ctx() -> Generator[BaseTest, None, None]:
    app = get_app()
    yield BaseTest(app.test_client, _TestHelper)


@pytest.fixture
def base_test() -> Generator[BaseTest, None, None]:
    with base_test_ctx() as base_test:
        yield base_test


class TestSanicGrpc:
    def test_create_user(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import CreateUserRequest

        with client_ctx() as client:
            for url in ("/api/user/create", "/api/static/user/create"):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(
                        url,
                        json={"uid": "10086", "user_name": "so1n", "pw": "123456", "sex": 0},
                        headers={"token": "token"},
                    )
                    assert response.body == b'{"code":0,"msg":"","data":{}}'
                    message: CreateUserRequest = queue.get(timeout=1)
                    assert message.uid == "10086"
                    assert message.user_name == "so1n"
                    assert message.password == "123456"
                    assert message.sex == 0

    def test_get_book(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookRequest

        with client_ctx() as client:
            for url in (
                "/api/book/get",
                "/api/static/book/get",
            ):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(url + "?isbn=xxxa", headers={"token": "token"})
                    assert json.loads(response.body.decode()) == {
                        "code": 0,
                        "data": {"book_author": "", "book_desc": "", "book_name": "", "book_url": "", "isbn": ""},
                        "msg": "",
                    }
                    queue.get(timeout=1)
                    message: GetBookRequest = queue.get(timeout=1)
                    assert message.isbn == "xxxa"

    def test_get_book_list(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookListRequest

        with client_ctx() as client:
            for url in (
                "/api/book/get-list",
                "/api/static/book/get-list",
            ):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(
                        url, json={"limit": 0, "next_create_time": "2023-04-10 18:44:36"}, headers={"token": "token"}
                    )
                    assert json.loads(response.body.decode()) == {"code": 0, "data": [], "msg": ""}
                    queue.get(timeout=1)
                    message: GetBookListRequest = queue.get(timeout=1)
                    assert message.limit == 0

    def test_get_book_like(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.social_pb2 import (
            GetBookLikesRequest,
            NestedGetBookLikesRequest,
        )

        with client_ctx() as client:
            for url in (
                "/api/book/get-book-like",
                "/api/book/get-book-like-other",
                "/api/static/book/get-book-like",
                "/api/static/book/get-book-like-other",
            ):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(url, json={"isbn": ["xxxa", "xxxb"]}, headers={"token": "token"})
                    assert json.loads(response.body.decode()) == {"code": 0, "data": {"result": []}, "msg": ""}
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
            for url in ("/api/user/login", "/api/static/user/login"):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(url, json={"uid": "10086", "password": "pw"})
                    assert response.body == b'{"code":0,"msg":"","data":{"uid":"","user_name":"","token":""}}'
                    message: LoginUserRequest = queue.get(timeout=1)
                    assert message.uid == "10086"
                    assert message.password == "pw"

    def test_logout(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import LogoutUserRequest

        with client_ctx() as client:
            for url in ("/api/user/logout", "/api/static/user/logout"):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(url, json={"uid": "10086"}, headers={"token": "token"})
                    assert response.body == b'{"code":0,"msg":"","data":{}}'
                    message: LogoutUserRequest = queue.get(timeout=1)
                    assert message.uid == "10086"
                    assert message.token == "token"

    def test_delete_fail_token(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import GetUidByTokenRequest

        with client_ctx() as client:
            for url in ("/api/user/delete", "/api/static/user/delete"):
                with grpc_request_test(client.app) as queue:
                    request, response = client.post(
                        url,
                        json={"uid": "10086"},
                        headers={"token": "fail_token"},
                    )
                    assert response.body == b'{"code":-1,"msg":"Not found user by token:fail_token"}'
                    message: GetUidByTokenRequest = queue.get(timeout=1)
                    assert message.token == "fail_token"

    def test_nested_demo(self) -> None:
        with client_ctx() as client:
            for url in ("/api/other/nested-demo", "/api/static/other/nested-demo"):
                with grpc_request_test(client.app):
                    body: bytes = client.post(url, headers={"token": "token"})[1].body
                    assert body == b'{"code":0,"msg":"","data":{"a":[{"map_demo":{"c":[{"a":1,"b":"foo"}]}}]}}'

    def test_grpc_openapi(self) -> None:
        with client_ctx() as client:
            grpc_test_openapi(client.app)
            grpc_test_openapi(client.app, url_prefix="/api/static", option_str="_by_option")

    def test_grpc_openapi_by_protobuf_file(self) -> None:
        with base_test_ctx() as base_test:
            base_test.grpc_openapi_by_protobuf_file(base_test.client.app, GrpcGatewayRoute)

    def test_grpc_openapi_by_option(self) -> None:
        with base_test_ctx() as base_test:
            base_test.grpc_openapi_by_option(base_test.client.app, GrpcGatewayRoute)
