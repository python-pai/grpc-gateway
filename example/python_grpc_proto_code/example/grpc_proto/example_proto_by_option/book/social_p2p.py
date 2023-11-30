# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.4.2
from datetime import datetime
from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_validator import check_one_of
from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator
import typing


class LikeBookRequest(BaseModel):

    isbn: str = Field(default="")
    like: bool = Field(default=False)
    uid: str = Field(default="")


class LikeBookMapRequest(BaseModel):

    like_map: typing.Dict[str, bool] = Field(default_factory=dict)
    uid: str = Field(default="")


class GetBookLikesRequest(BaseModel):

    isbn: typing.List[str] = Field(default_factory=list)


class GetBookLikesResult(BaseModel):

    isbn: str = Field(default="")
    book_like: int = Field(default=0)


class GetBookLikesListResult(BaseModel):

    result: typing.List[GetBookLikesResult] = Field(default_factory=list)


class CommentBookRequest(BaseModel):

    isbn: str = Field(default="")
    content: str = Field(default="")
    uid: str = Field(default="")


class GetBookCommentRequest(BaseModel):

    _one_of_dict = {"GetBookCommentRequest._limit": {"fields": {"limit"}}, "GetBookCommentRequest._next_create_time": {"fields": {"next_create_time"}}}
    one_of_validator = model_validator(mode="before")(check_one_of)

    isbn: str = Field(default="")
    next_create_time: typing.Optional[datetime] = Field(default_factory=datetime.now)
    limit: typing.Optional[int] = Field(default=0)


class GetBookCommentResult(BaseModel):

    isbn: str = Field(default="")
    content: str = Field(default="")
    uid: str = Field(default="")
    create_time: datetime = Field(default_factory=datetime.now)


class GetBookCommentListResult(BaseModel):

    result: typing.List[GetBookCommentResult] = Field(default_factory=list)


class NestedGetBookLikesRequest(BaseModel):

    nested: GetBookLikesRequest = Field()
