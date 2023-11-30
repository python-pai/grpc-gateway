# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.4.2
from datetime import datetime
from google.protobuf.message import Message  # type: ignore
from pait.field.request_resource import Query
from pydantic import BaseModel
from pydantic import Field
import typing


class CreateBookRequest(BaseModel):

    isbn: str = Field(default="")
    book_name: str = Field(default="")
    book_author: str = Field(default="")
    book_desc: str = Field(default="")
    book_url: str = Field(default="")


class DeleteBookRequest(BaseModel):

    isbn: str = Field(default="")


class GetBookRequest(BaseModel):

    isbn: str = Query(default="")
    not_use_field1: str = Field(default="")
    not_use_field2: str = Field(default="")


class GetBookResult(BaseModel):

    isbn: str = Field(default="")
    book_name: str = Field(default="")
    book_author: str = Field(default="")
    book_desc: str = Field(default="")
    book_url: str = Field(default="")
    create_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)


class GetBookListRequest(BaseModel):

    next_create_time: typing.Optional[datetime] = Field(default_factory=datetime.now)
    limit: int = Field(default=0)


class GetBookListResult(BaseModel):

    result: typing.List[GetBookResult] = Field(default_factory=list)
