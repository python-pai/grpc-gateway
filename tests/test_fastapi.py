import asyncio
import json
from contextlib import contextmanager
from queue import Queue
from typing import Generator, Tuple

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pait.app.starlette import TestHelper as _TestHelper
from pait.exceptions import PaitBaseException
from pydantic import ValidationError

from example.fastapi_example import grpc_route
from example.fastapi_example.utils import api_exception
from grpc_gateway.base_gateway import _grpc_gateway_title_set
from grpc_gateway.dynamic_gateway.gateway import AsyncGrpcGatewayRoute as GrpcGatewayRoute
from tests.base_api_test import BaseTest
from tests.conftest import grpc_request_test, grpc_test_openapi


def get_app() -> FastAPI:
    # starlette run after sanic
    # fix starlette.testclient get_event_loop status is close
    # def get_event_loop() -> asyncio.AbstractEventLoop:
    #     try:
    #         loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    #         if loop.is_closed():
    #             loop = asyncio.new_event_loop()
    #     except RuntimeError:
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)
    #     return loop
    #
    # mocker.patch("asyncio.get_event_loop").return_value = get_event_loop()
    # asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        asyncio.set_event_loop(asyncio.new_event_loop())

    _grpc_gateway_title_set.clear()
    app = FastAPI()
    app.add_exception_handler(PaitBaseException, api_exception)
    app.add_exception_handler(ValidationError, api_exception)
    app.add_exception_handler(RuntimeError, api_exception)
    return app


@contextmanager
def client_ctx() -> Generator[TestClient, None, None]:
    with TestClient(get_app()) as client:
        yield client


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with client_ctx() as client:
        yield client


@contextmanager
def base_test_ctx() -> Generator[BaseTest, None, None]:
    with client_ctx() as client:
        yield BaseTest(client, _TestHelper)


@pytest.fixture
def base_test() -> Generator[BaseTest, None, None]:
    with base_test_ctx() as base_test:
        yield base_test


@contextmanager
def grpc_client() -> Generator[Tuple[TestClient, Queue], None, None]:
    app = get_app()
    grpc_route.add_grpc_gateway_route(app)
    with grpc_request_test(app) as queue:
        with TestClient(app) as client:
            yield client, queue


class TestStarletteGrpc:
    def test_create_user(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import CreateUserRequest

        with grpc_client() as grpc_client_tuple:
            for url in ("/api/user/create", "/api/static/user/create"):
                client, queue = grpc_client_tuple
                body: bytes = client.post(
                    url,
                    json={"uid": "10086", "user_name": "so1n", "pw": "123456", "sex": 0},
                    headers={"token": "token"},
                ).content
                assert body == b'{"code":0,"msg":"","data":{}}'
                message: CreateUserRequest = queue.get(timeout=1)
                assert message.uid == "10086"
                assert message.user_name == "so1n"
                assert message.password == "123456"
                assert message.sex == 0

    def test_get_book(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookRequest

        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple

            for url in ("/api/book/get", "/api/static/book/get"):
                body: bytes = client.post(url + "?isbn=xxxa", headers={"token": "token"}).content
                assert json.loads(body.decode()) == {
                    "code": 0,
                    "data": {"book_author": "", "book_desc": "", "book_name": "", "book_url": "", "isbn": ""},
                    "msg": "",
                }
                queue.get(timeout=1)
                message: GetBookRequest = queue.get(timeout=1)
                assert message.isbn == "xxxa"

    def test_get_book_list(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookListRequest

        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple

            for url in ("/api/book/get-list", "/api/static/book/get-list"):
                body: bytes = client.post(
                    url, json={"limit": 0, "next_create_time": "2023-04-10 18:44:36"}, headers={"token": "token"}
                ).content
                assert json.loads(body.decode()) == {"code": 0, "data": [], "msg": ""}
                queue.get(timeout=1)
                message: GetBookListRequest = queue.get(timeout=1)
                assert message.limit == 0

    def test_get_book_like(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.social_pb2 import (
            GetBookLikesRequest,
            NestedGetBookLikesRequest,
        )

        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple

            for url in (
                "/api/book/get-book-like",
                "/api/book/get-book-like-other",
                "/api/static/book/get-book-like",
                "/api/static/book/get-book-like-other",
            ):
                body: bytes = client.post(url, json={"isbn": ["xxxa", "xxxb"]}, headers={"token": "token"}).content
                assert json.loads(body.decode()) == {"code": 0, "data": {"result": []}, "msg": ""}
                queue.get(timeout=1)
                if not url.endswith("other"):
                    message1: GetBookLikesRequest = queue.get(timeout=1)
                    assert message1.isbn == ["xxxa", "xxxb"]
                else:
                    message2: NestedGetBookLikesRequest = queue.get(timeout=1)
                    assert message2.nested.isbn == ["xxxa", "xxxb"]

    def test_login(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import LoginUserRequest

        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple
            for url in ("/api/user/login", "/api/static/user/login"):
                body: bytes = client.post(url, json={"uid": "10086", "password": "pw"}).content
                assert body == b'{"code":0,"msg":"","data":{"uid":"","user_name":"","token":""}}'
                message: LoginUserRequest = queue.get(timeout=1)
                assert message.uid == "10086"
                assert message.password == "pw"

    def test_logout(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import LogoutUserRequest

        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple
            for url in ("/api/user/logout", "/api/static/user/logout"):
                body: bytes = client.post(url, json={"uid": "10086"}, headers={"token": "token"}).content
                assert body == b'{"code":0,"msg":"","data":{}}'
                message: LogoutUserRequest = queue.get(timeout=1)
                assert message.uid == "10086"
                assert message.token == "token"

    def test_delete_fail_token(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import GetUidByTokenRequest

        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple
            for url in ("/api/user/delete", "/api/static/user/delete"):
                body: bytes = client.post(
                    url,
                    json={"uid": "10086"},
                    headers={"token": "fail_token"},
                ).content
                assert body == b'{"code":-1,"msg":"Not found user by token:fail_token"}'
                message: GetUidByTokenRequest = queue.get(timeout=1)
                assert message.token == "fail_token"

    def test_nested_demo(self) -> None:
        with grpc_client() as grpc_client_tuple:
            client, queue = grpc_client_tuple

            for url in ("/api/other/nested-demo", "/api/static/other/nested-demo"):
                with grpc_request_test(client.app):
                    body: bytes = client.post(url, headers={"token": "token"}).content
                    assert body == b'{"code":0,"msg":"","data":{"a":[{"map_demo":{"c":[{"a":1,"b":"foo"}]}}]}}'

    def test_grpc_openapi(self) -> None:
        app = get_app()
        grpc_route.add_grpc_gateway_route(app)

        with TestClient(app) as client:
            grpc_test_openapi(client.app)
            grpc_test_openapi(client.app, url_prefix="/api/static", option_str="_by_option")

    def test_grpc_openapi_by_protobuf_file(self, base_test: BaseTest) -> None:
        base_test.grpc_openapi_by_protobuf_file(base_test.client.app, GrpcGatewayRoute)

    def test_grpc_openapi_by_option(self) -> None:
        with base_test_ctx() as base_test:
            base_test.grpc_openapi_by_option(base_test.client.app, GrpcGatewayRoute)
