# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.4.2
import typing
from datetime import datetime

from google.protobuf.message import Message  # type: ignore
from pait.field.request_resource import Query
from pydantic import BaseModel, Field


class CreateBookRequest(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})
    book_name: str = Field(default="", json_schema_extra={})
    book_author: str = Field(default="", json_schema_extra={})
    book_desc: str = Field(default="", json_schema_extra={})
    book_url: str = Field(default="", json_schema_extra={})


class DeleteBookRequest(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})


class GetBookRequest(BaseModel):
    isbn: str = Query(default="", json_schema_extra={})
    not_use_field1: str = Field(default="", json_schema_extra={})
    not_use_field2: str = Field(default="", json_schema_extra={})


class GetBookResult(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})
    book_name: str = Field(default="", json_schema_extra={})
    book_author: str = Field(default="", json_schema_extra={})
    book_desc: str = Field(default="", json_schema_extra={})
    book_url: str = Field(default="", json_schema_extra={})
    create_time: datetime = Field(default_factory=datetime.now, json_schema_extra={})
    update_time: datetime = Field(default_factory=datetime.now, json_schema_extra={})


class GetBookListRequest(BaseModel):
    next_create_time: typing.Optional[datetime] = Field(default_factory=datetime.now, json_schema_extra={})
    limit: int = Field(default=0, json_schema_extra={})


class GetBookListResult(BaseModel):
    result: typing.List[GetBookResult] = Field(default_factory=list, json_schema_extra={})
