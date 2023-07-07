from typing import Any, Type

from pait.app.base import BaseTestHelper
from pait.openapi.openapi import OpenAPI

from example.common.response_model import gen_response_model_handle
from grpc_gateway.dynamic_gateway.gateway import DynamicGrpcGatewayRoute
from tests.conftest import grpc_test_openapi


class BaseTest(object):
    def __init__(self, client: Any, test_helper: Type[BaseTestHelper]):
        self.client: Any = client
        self.test_helper: Type[BaseTestHelper] = test_helper

    @staticmethod
    def grpc_openapi_by_protobuf_file(app: Any, grpc_gateway_route: Type[DynamicGrpcGatewayRoute]) -> None:
        import os

        from example.grpc_common.python_example_proto_code.example_proto.book import manager_pb2_grpc, social_pb2_grpc
        from example.grpc_common.python_example_proto_code.example_proto.user import user_pb2_grpc

        project_path: str = os.getcwd().split("pait/")[0]
        if project_path.endswith("pait"):
            project_path += "/"
        elif not project_path.endswith("pait/"):
            project_path = os.path.join(project_path, "pait/")
        grpc_path: str = project_path + "example/grpc_common/"

        from pathlib import Path

        if not Path(grpc_path).exists():
            return

        prefix: str = "/api-test"

        grpc_gateway_route(
            app,
            user_pb2_grpc.UserStub,
            social_pb2_grpc.BookSocialStub,
            manager_pb2_grpc.BookManagerStub,
            prefix=prefix + "/",
            title="Grpc-test",
            parse_msg_desc=grpc_path,
            gen_response_model_handle=gen_response_model_handle,
        )
        grpc_test_openapi(app, url_prefix=prefix)

    @staticmethod
    def grpc_openapi_by_option(app: Any, grpc_gateway_route: Type[DynamicGrpcGatewayRoute]) -> None:
        from example.grpc_common.python_example_proto_code.example_proto_by_option.book import (
            manager_pb2_grpc,
            social_pb2_grpc,
        )
        from example.grpc_common.python_example_proto_code.example_proto_by_option.user import user_pb2_grpc

        prefix: str = "/api-test-by-option"

        grpc_gateway_route(
            app,
            user_pb2_grpc.UserStub,
            social_pb2_grpc.BookSocialStub,
            manager_pb2_grpc.BookManagerStub,
            prefix=prefix + "/",
            title="Grpc-test",
            gen_response_model_handle=gen_response_model_handle,
        )
        grpc_test_openapi(app, url_prefix=prefix, option_str="_by_option")

        pait_openapi: OpenAPI = OpenAPI(app)
        assert (
            pait_openapi.dict["paths"]["/api-test-by-option/book/get-book-like"]["post"]["pait_info"]["pait_id"][:-1]
            == pait_openapi.dict["paths"]["/api-test-by-option/book_social_by_option-BookSocial/get_book_like"]["get"][
                "pait_info"
            ]["pait_id"][:-1]
        )
