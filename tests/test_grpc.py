from typing import Dict, List

import pytest
from google.protobuf.empty_pb2 import Empty  # type: ignore
from pait import _pydanitc_adapter
from pait.util import gen_example_dict_from_pydantic_base_model
from pydantic import BaseModel, Field

from example.grpc_common.python_example_proto_code.example_proto_by_option.user import user_pb2
from grpc_gateway.dynamic_gateway.gateway import _gen_response_model_handle
from grpc_gateway.dynamic_gateway.inspect import GrpcMethodModel
from grpc_gateway.model import GrpcServiceOptionModel
from grpc_gateway.protobuf_types import Message
from grpc_gateway.rebuild_message import rebuild_dict, rebuild_message_type


class Demo(BaseModel):
    class SubDemo(BaseModel):
        class SubSubDemo(BaseModel):
            aaa: int = Field()
            bbb: int = Field()

        aa: int = Field()
        bb: int = Field()
        cc: SubSubDemo = Field()

    a: int = Field()
    b: int = Field()
    c: SubDemo = Field()


class ComplexDemo(BaseModel):
    class SubDemo(BaseModel):
        class SubSUbDemo(BaseModel):
            class SubSubSubDemo(BaseModel):
                d: str = Field()

            c: Dict[int, SubSubSubDemo] = Field()

        b: Dict[str, SubSUbDemo]

    a: List[SubDemo]


class TestUtil:
    def test_gen_response_model_handle(self) -> None:
        # invoke_name: str
        # grpc_method_url: str
        # alias_grpc_method_url: str
        # grpc_service_option_model: GrpcServiceOptionModel
        # # func: Callable
        # request: Type[Message] = Message
        # response: Type[Message] = Message
        assert issubclass(
            _gen_response_model_handle(
                GrpcMethodModel(
                    invoke_name="",
                    grpc_method_url="",
                    alias_grpc_method_url="",
                    request=Message,
                    response=Empty,
                    grpc_service_option_model=GrpcServiceOptionModel(),
                )
            ).response_data,
            dict,
        )
        assert issubclass(
            _gen_response_model_handle(
                GrpcMethodModel(
                    invoke_name="",
                    grpc_method_url="",
                    alias_grpc_method_url="",
                    request=Message,
                    response=user_pb2.GetUidByTokenResult,
                    grpc_service_option_model=GrpcServiceOptionModel(),
                )
            ).response_data,
            BaseModel,
        )

    def test_rebuild_message_type(self) -> None:
        # test not option param
        assert int == rebuild_message_type(int, "")

        # test type error
        with pytest.raises(TypeError):
            rebuild_message_type(int, "", exclude_column_name=["a", "b"])

        # test exclude_column
        new_message = rebuild_message_type(Demo, "", exclude_column_name=["a", "b"])
        assert issubclass(new_message, BaseModel)
        assert len(_pydanitc_adapter.model_fields(new_message)) == 1
        if _pydanitc_adapter.is_v1:
            for column in ["name", "type_", "required"]:
                assert getattr(_pydanitc_adapter.model_fields(new_message)["c"], column) == getattr(
                    _pydanitc_adapter.model_fields(Demo)["c"], column
                )
        else:
            assert getattr(_pydanitc_adapter.model_fields(new_message)["c"], "annotation") == getattr(
                _pydanitc_adapter.model_fields(Demo)["c"], "annotation"
            )
            assert (
                getattr(_pydanitc_adapter.model_fields(new_message)["c"], "is_required")()
                == getattr(_pydanitc_adapter.model_fields(Demo)["c"], "is_required")()
            )
        # test nested
        new_message = rebuild_message_type(Demo, "", nested=["c", "cc"])
        assert issubclass(new_message, BaseModel)
        for model_column in ["aaa", "bbb"]:
            if _pydanitc_adapter.is_v1:
                for column in ["name", "type_", "required"]:
                    for column in ["name", "type_", "required"]:
                        assert getattr(_pydanitc_adapter.model_fields(new_message)[model_column], column) == getattr(
                            _pydanitc_adapter.model_fields(Demo.SubDemo.SubSubDemo)[model_column], column
                        )
            else:
                assert getattr(_pydanitc_adapter.model_fields(new_message)[model_column], "annotation") == getattr(
                    _pydanitc_adapter.model_fields(Demo.SubDemo.SubSubDemo)[model_column], "annotation"
                )
                assert (
                    getattr(_pydanitc_adapter.model_fields(new_message)[model_column], "is_required")()
                    == getattr(_pydanitc_adapter.model_fields(Demo.SubDemo.SubSubDemo)[model_column], "is_required")()
                )
        # Test complex nesteds

        new_message = rebuild_message_type(ComplexDemo, "", nested=["a", "$[]", "b", "${}", "$.c"])
        assert new_message.__args__[0].__args__[0] == str
        assert new_message.__args__[0].__args__[1] == ComplexDemo.SubDemo.SubSUbDemo
        if _pydanitc_adapter.is_v1:
            assert new_message.__args__[0].__args__[1].__fields__["c"].outer_type_.__args__[0] == int
            assert (
                new_message.__args__[0].__args__[1].__fields__["c"].outer_type_.__args__[1]
                == ComplexDemo.SubDemo.SubSUbDemo.SubSubSubDemo
            )
        else:
            assert new_message.__args__[0].__args__[1].__fields__["c"].annotation.__args__[0] == int
            assert (
                new_message.__args__[0].__args__[1].__fields__["c"].annotation.__args__[1]
                == ComplexDemo.SubDemo.SubSUbDemo.SubSubSubDemo
            )

    def test_rebuild_dict(self) -> None:
        # test not option param
        assert {} == rebuild_dict({})

        # test exclude_column
        assert rebuild_dict(gen_example_dict_from_pydantic_base_model(Demo), exclude_column_name=["a", "b"]) == {
            "c": {"aa": 0, "bb": 0, "cc": {"aaa": 0, "bbb": 0}}
        }

        # test nested
        assert rebuild_dict(gen_example_dict_from_pydantic_base_model(Demo), nested=["c", "cc"]) == {"aaa": 0, "bbb": 0}

        # Test complex nesteds
        assert rebuild_dict({"a": [{"b": {"1": {"c": {2: {"d": ""}}}}}]}, nested=["a", "$[]", "b", "${}", "$.c"]) == [
            {"1": {"c": {2: {"d": ""}}}}
        ]
