from typing import Any, Dict, List

import pytest
from pait import _pydanitc_adapter
from pait.util import gen_example_dict_from_pydantic_base_model
from pydantic import BaseModel, Field

from grpc_gateway.model import field_validator
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

    @field_validator("a", "c")
    @classmethod
    def validator_a(cls, value: Any) -> Any:
        return value

    @_pydanitc_adapter.model_validator(mode="before")
    @classmethod
    def model_v(cls, value: Any) -> Any:
        return value


class ComplexDemo(BaseModel):
    class SubDemo(BaseModel):
        class SubSUbDemo(BaseModel):
            class SubSubSubDemo(BaseModel):
                d: str = Field()

            c: Dict[int, SubSubSubDemo] = Field()

        b: Dict[str, SubSUbDemo]

    a: List[SubDemo]


class TestRebuildMessage:
    def test_rebuild_message_type(self) -> None:
        # test not option param
        assert int == rebuild_message_type(int, "")

        # test type error
        with pytest.raises(TypeError):
            rebuild_message_type(int, "", exclude_column_name=["a", "b"])

        # test exclude_column
        new_message = rebuild_message_type(Demo, "", exclude_column_name=["a", "b"])
        assert issubclass(new_message, BaseModel)

        if _pydanitc_adapter.is_v1:
            assert "c" in new_message.__validators__  # type: ignore
            assert "model_v" == new_message.__pre_root_validators__[0].__name__  # type: ignore
            assert len(new_message.__pre_root_validators__) == 1  # type: ignore
        else:
            assert "c" in new_message.__pydantic_decorators__.field_validators["validator_a"].info.fields
            assert "model_v" in new_message.__pydantic_decorators__.model_validators

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
        message_args = new_message.__args__  # type: ignore
        assert message_args[0].__args__[0] == str
        assert message_args[0].__args__[1] == ComplexDemo.SubDemo.SubSUbDemo
        if _pydanitc_adapter.is_v1:
            assert message_args[0].__args__[1].__fields__["c"].outer_type_.__args__[0] == int
            assert (
                message_args[0].__args__[1].__fields__["c"].outer_type_.__args__[1]
                == ComplexDemo.SubDemo.SubSUbDemo.SubSubSubDemo
            )
        else:
            assert message_args[0].__args__[1].__fields__["c"].annotation.__args__[0] == int
            assert (
                message_args[0].__args__[1].__fields__["c"].annotation.__args__[1]
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
