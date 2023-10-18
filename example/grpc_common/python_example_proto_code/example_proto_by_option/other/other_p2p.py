# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.4.2
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing





class DemoMessage(BaseModel):

    a: int = Field(default=0, json_schema_extra={})
    b: str = Field(default="", json_schema_extra={})



class SubSubSubNestedMessage(BaseModel):

    repeated_demo: typing.List[DemoMessage] = Field(default_factory=list, json_schema_extra={})



class SubSubNestedMessage(BaseModel):

    map_demo: typing.Dict[str, SubSubSubNestedMessage] = Field(default_factory=dict, json_schema_extra={})



class SubNestedMessage(BaseModel):

    repeated_demo: typing.List[SubSubNestedMessage] = Field(default_factory=list, json_schema_extra={})



class NestedMessage(BaseModel):

    map_demo: typing.Dict[str, SubNestedMessage] = Field(default_factory=dict, json_schema_extra={})
