import pytest
from pait import _pydanitc_adapter

from grpc_gateway.model import BuildMessageModel, RequestBuildMessageModel, field_validator

from .util import gen_demo_module, get_grpc_service_model_option


class TestBuildMessage:
    def test_field_validator(self) -> None:
        if not _pydanitc_adapter.is_v1:
            return
        with pytest.raises(ValueError):
            field_validator("a", mode="a")

    def test_build_message(self) -> None:
        a_model = BuildMessageModel(nested=["a", "b", "c"], exclude_column_name=["1", "2", "3"])
        b_model = BuildMessageModel(nested="a/b/c", exclude_column_name="1,2,3")
        assert _pydanitc_adapter.model_dump(a_model) == _pydanitc_adapter.model_dump(b_model)
        assert a_model.has_value()
        assert b_model.has_value()

    def test_request_build_message(self) -> None:
        a_model = RequestBuildMessageModel(exclude_column_name=[], nested="a/$b/c")
        b_model = RequestBuildMessageModel(exclude_column_name=[], nested="a/c")
        assert _pydanitc_adapter.model_dump(a_model) == _pydanitc_adapter.model_dump(b_model)


class TestGetGrpcServiceModelFromOptionMessage:
    def test_demo(self) -> None:
        demo_grpc_service_model = get_grpc_service_model_option(gen_demo_module)
        assert demo_grpc_service_model["use_all_attr"][0].name == ""
        assert demo_grpc_service_model["use_all_attr"][0].group == "demo"
        assert demo_grpc_service_model["use_all_attr"][0].tag == [("demo_tag", "test protobuf tag")]
        assert demo_grpc_service_model["use_all_attr"][0].summary == "This is a summary"
        assert demo_grpc_service_model["use_all_attr"][0].desc == "This is a desc"
        assert demo_grpc_service_model["use_all_attr"][0].author == ("so1n",)
        assert demo_grpc_service_model["use_all_attr"][0].url == "/demo/use-all-attr"
        assert demo_grpc_service_model["use_all_attr"][0].http_method == "GET"
        assert demo_grpc_service_model["use_all_attr"][1].enable is False
        assert demo_grpc_service_model["use_all_attr"][1].http_method == "POST"
        assert demo_grpc_service_model["use_all_attr"][2].http_method == "POST"
        assert demo_grpc_service_model["use_all_attr"][2].url == "/demo/use-all-attr-any"
        # webframework will test nested and exclude_column_name
