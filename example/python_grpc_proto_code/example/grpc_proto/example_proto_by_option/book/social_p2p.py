# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.4.2
import typing
from datetime import datetime

from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_validator import check_one_of
from pydantic import BaseModel, Field, model_validator


class LikeBookRequest(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})
    like: bool = Field(default=False, json_schema_extra={})
    uid: str = Field(default="", json_schema_extra={})


class LikeBookMapRequest(BaseModel):
    like_map: typing.Dict[str, bool] = Field(default_factory=dict, json_schema_extra={})
    uid: str = Field(default="", json_schema_extra={})


class GetBookLikesRequest(BaseModel):
    isbn: typing.List[str] = Field(default_factory=list, json_schema_extra={})


class GetBookLikesResult(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})
    book_like: int = Field(default=0, json_schema_extra={})


class GetBookLikesListResult(BaseModel):
    result: typing.List[GetBookLikesResult] = Field(default_factory=list, json_schema_extra={})


class CommentBookRequest(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})
    content: str = Field(default="", json_schema_extra={})
    uid: str = Field(default="", json_schema_extra={})


class GetBookCommentRequest(BaseModel):
    _one_of_dict = {
        "GetBookCommentRequest._limit": {"fields": {"limit"}},
        "GetBookCommentRequest._next_create_time": {"fields": {"next_create_time"}},
    }
    one_of_validator = model_validator(mode="before")(check_one_of)

    isbn: str = Field(default="", json_schema_extra={})
    next_create_time: typing.Optional[datetime] = Field(default_factory=datetime.now, json_schema_extra={})
    limit: typing.Optional[int] = Field(default=0, json_schema_extra={})


class GetBookCommentResult(BaseModel):
    isbn: str = Field(default="", json_schema_extra={})
    content: str = Field(default="", json_schema_extra={})
    uid: str = Field(default="", json_schema_extra={})
    create_time: datetime = Field(default_factory=datetime.now, json_schema_extra={})


class GetBookCommentListResult(BaseModel):
    result: typing.List[GetBookCommentResult] = Field(default_factory=list, json_schema_extra={})


class NestedGetBookLikesRequest(BaseModel):
    nested: GetBookLikesRequest = Field(json_schema_extra={})
