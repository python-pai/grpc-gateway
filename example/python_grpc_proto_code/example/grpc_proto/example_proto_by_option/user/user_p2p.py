# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.4.2
from enum import IntEnum
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field

class SexType(IntEnum):
    man = 0
    women = 1



class CreateUserRequest(BaseModel):

    uid: str = Field(title="UID", description="user union id", example="10086")
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    password: str = Field(default="", alias="pw", description="user password", min_length=6, max_length=18, example="123456")
    sex: SexType = Field(default=0)


class DeleteUserRequest(BaseModel):

    uid: str = Field(default="")


class LoginUserRequest(BaseModel):

    uid: str = Field(default="")
    password: str = Field(default="")


class LoginUserResult(BaseModel):

    uid: str = Field(default="", title="UID", description="user union id", example="10086")
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    token: str = Field(default="", description="user token")


class LogoutUserRequest(BaseModel):

    uid: str = Field(default="")


class GetUidByTokenRequest(BaseModel):

    token: str = Field(default="")


class GetUidByTokenResult(BaseModel):

    uid: str = Field(default="")
