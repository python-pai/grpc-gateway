import json

from pait.app.tornado import TestHelper as _TestHelper
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from example.tornado_example import grpc_route
from tests.base_api_test import BaseTest
from tests.conftest import grpc_request_test, grpc_test_openapi


class BaseTestTornado(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        return Application()

    @property
    def base_test(self) -> BaseTest:
        return BaseTest(self, _TestHelper)

    def get_url(self, path: str) -> str:
        """Returns an absolute url for the given path on the test server."""
        return "%s://localhost:%s%s" % (self.get_protocol(), self.get_http_port(), path)


class TestTornadoGrpc(BaseTestTornado):
    # def test_create_user(self) -> None:
    #     main_example.add_grpc_gateway_route(self._app)
    #     main_example.add_api_doc_route(self._app)
    #
    #     self._app.settings["before_server_start"]()
    #
    #     def _(request_dict: dict) -> None:
    #         body: bytes = self.fetch("/api/user/create", body=json.dumps(request_dict).encode(), method="POST").body
    #         assert body == b"{}"
    #
    #     grpc_request_test(self._app, _)
    #
    def test_create_user(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import CreateUserRequest

        self.setUp()

        grpc_route.add_grpc_gateway_route(self._app)

        with grpc_request_test(self._app) as queue:
            for url in ("/api/user/create", "/api/static/user/create"):
                body: bytes = self.fetch(
                    url,
                    method="POST",
                    body='{"uid": "10086", "user_name": "so1n", "pw": "123456", "sex": 0}',
                    headers={"token": "token"},
                ).body
                assert body == b'{"code": 0, "msg": "", "data": {}}'
                message: CreateUserRequest = queue.get(timeout=1)
                assert message.uid == "10086"
                assert message.user_name == "so1n"
                assert message.password == "123456"
                assert message.sex == 0

    def test_get_book(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.manager_pb2 import GetBookRequest

        self.setUp()

        grpc_route.add_grpc_gateway_route(self._app)
        with grpc_request_test(self._app) as queue:
            for url in ("/api/book/get", "/api/static/book/get"):
                body: bytes = self.fetch(url + "?isbn=xxxa", method="POST", headers={"token": "token"}, body="").body
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

        self.setUp()

        grpc_route.add_grpc_gateway_route(self._app)
        with grpc_request_test(self._app) as queue:
            for url in ("/api/book/get-list", "/api/static/book/get-list"):
                body: bytes = self.fetch(
                    url,
                    method="POST",
                    body='{"limit": 0, "next_create_time": "2023-04-10 18:44:36"}',
                    headers={"token": "token"},
                ).body
                assert json.loads(body.decode()) == {"code": 0, "data": [], "msg": ""}
                queue.get(timeout=1)
                message: GetBookListRequest = queue.get(timeout=1)
                assert message.limit == 0

    def test_get_book_like(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.book.social_pb2 import (
            GetBookLikesRequest,
            NestedGetBookLikesRequest,
        )

        self.setUp()

        grpc_route.add_grpc_gateway_route(self._app)
        with grpc_request_test(self._app) as queue:
            for url in (
                "/api/book/get-book-like",
                "/api/book/get-book-like-other",
                "/api/static/book/get-book-like",
                "/api/static/book/get-book-like-other",
            ):
                body: bytes = self.fetch(
                    url, method="POST", body='{"isbn": ["xxxa", "xxxb"]}', headers={"token": "token"}
                ).body
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

        self.setUp()
        grpc_route.add_grpc_gateway_route(self._app)

        with grpc_request_test(self._app) as queue:
            for url in ("/api/user/login", "/api/static/user/login"):
                body: bytes = self.fetch(url, method="POST", body='{"uid": "10086", "password": "pw"}').body
                assert body == b'{"code": 0, "msg": "", "data": {"uid": "", "user_name": "", "token": ""}}'
                message: LoginUserRequest = queue.get(timeout=1)
                assert message.uid == "10086"
                assert message.password == "pw"

    def test_logout(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import LogoutUserRequest

        self.setUp()
        grpc_route.add_grpc_gateway_route(self._app)

        with grpc_request_test(self._app) as queue:
            for url in ("/api/user/logout", "/api/static/user/logout"):
                body: bytes = self.fetch(url, method="POST", body='{"uid": "10086"}', headers={"token": "token"}).body
                assert body == b'{"code": 0, "msg": "", "data": {}}'
                message: LogoutUserRequest = queue.get(timeout=1)
                assert message.uid == "10086"
                assert message.token == "token"

    def test_delete_fail_token(self) -> None:
        from example.grpc_common.python_example_proto_code.example_proto.user.user_pb2 import GetUidByTokenRequest

        self.setUp()

        grpc_route.add_grpc_gateway_route(self._app)

        with grpc_request_test(self._app) as queue:
            for url in ("/api/user/delete", "/api/static/user/delete"):
                body: bytes = self.fetch(
                    url,
                    method="POST",
                    body='{"uid": "10086"}',
                    headers={"token": "fail_token"},
                ).body
                assert body == b'{"code": -1, "msg": "Not found user by token:fail_token"}'
                message: GetUidByTokenRequest = queue.get(timeout=1)
                assert message.token == "fail_token"

    def test_nested_demo(self) -> None:
        self.setUp()

        grpc_route.add_grpc_gateway_route(self._app)
        with grpc_request_test(self._app):
            for url in ("/api/other/nested-demo", "/api/static/other/nested-demo"):
                body: bytes = self.fetch(url, body="{}", method="POST", headers={"token": "token"}).body
                assert body == b'{"code": 0, "msg": "", "data": {"a": [{"map_demo": {"c": [{"a": 1, "b": "foo"}]}}]}}'

    def test_grpc_openapi(self) -> None:
        grpc_route.add_grpc_gateway_route(self._app)

        grpc_test_openapi(self._app)
        grpc_test_openapi(self._app, url_prefix="/api/static", option_str="_by_option")

    def test_grpc_openapi_by_protobuf_file(self) -> None:
        from pait.grpc import AsyncGrpcGatewayRoute as GrpcGatewayRoute

        self.base_test.grpc_openapi_by_protobuf_file(self._app, GrpcGatewayRoute)

    def test_grpc_openapi_by_option(self) -> None:
        from pait.grpc import AsyncGrpcGatewayRoute as GrpcGatewayRoute

        self.setUp()
        self.base_test.grpc_openapi_by_option(self._app, GrpcGatewayRoute)
