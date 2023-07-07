# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.1.7.4](https://github.com/so1n/protobuf_to_pydantic)
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing





class DemoMessage(BaseModel):

    a: int = Field(default=0)
    b: str = Field(default="")



class SubSubSubNestedMessage(BaseModel):

    repeated_demo: typing.List[DemoMessage] = Field(default_factory=list)



class SubSubNestedMessage(BaseModel):

    map_demo: typing.Dict[str, SubSubSubNestedMessage] = Field(default_factory=dict)



class SubNestedMessage(BaseModel):

    repeated_demo: typing.List[SubSubNestedMessage] = Field(default_factory=list)



class NestedMessage(BaseModel):

    map_demo: typing.Dict[str, SubNestedMessage] = Field(default_factory=dict)
