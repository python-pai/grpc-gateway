# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.2](https://github.com/so1n/protobuf_to_pydantic)
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

    uid: str = Field(title="UID", description="user union id", json_schema_extra={"example": "10086"})
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, json_schema_extra={"example": "so1n"})
    password: str = Field(default="", alias="pw", description="user password", min_length=6, max_length=18, json_schema_extra={"example": "123456"})
    sex: SexType = Field(default=0, json_schema_extra={})



class DeleteUserRequest(BaseModel):

    uid: str = Field(default="", json_schema_extra={})



class LoginUserRequest(BaseModel):

    uid: str = Field(default="", json_schema_extra={})
    password: str = Field(default="", json_schema_extra={})



class LoginUserResult(BaseModel):

    uid: str = Field(default="", title="UID", description="user union id", json_schema_extra={"example": "10086"})
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, json_schema_extra={"example": "so1n"})
    token: str = Field(default="", description="user token", json_schema_extra={})



class LogoutUserRequest(BaseModel):

    uid: str = Field(default="", json_schema_extra={})



class GetUidByTokenRequest(BaseModel):

    token: str = Field(default="", json_schema_extra={})



class GetUidByTokenResult(BaseModel):

    uid: str = Field(default="", json_schema_extra={})
