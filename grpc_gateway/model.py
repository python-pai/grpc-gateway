import logging
from typing import Any, Callable, List, Tuple, Union

from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from pait import _pydanitc_adapter
from pydantic import BaseModel, Field

if _pydanitc_adapter.is_v1:
    from pydantic import validator as _field_validator  # type: ignore

    def field_validator(*fields: str, mode: str) -> Callable[[Any], Any]:  # type: ignore
        pre = None
        if mode == "before":
            pre = True
        elif mode == "after":
            pre = False
        else:
            raise ValueError(f"Not support mode: `{mode}`")

        return _field_validator(*fields, pre=pre)

else:
    from pydantic import field_validator as _field_validator  # type: ignore

    field_validator = _field_validator  # type: ignore


class BuildMessageModel(BaseModel):
    exclude_column_name: list = Field(default_factory=list)
    nested: list = Field(default_factory=list)

    def has_value(self) -> bool:
        return bool(self.exclude_column_name) or bool(self.nested)

    @field_validator("exclude_column_name", mode="before")
    def exclude_column_name_validator(cls, v: Union[str, list]) -> list:
        if isinstance(v, str):
            return [i for i in v.split(",") if i]
        return v

    @field_validator("nested", mode="before")
    def nested_validator(cls, v: Union[str, list]) -> list:
        if isinstance(v, str):
            return [i for i in v.split("/") if i]
        return v


class RequestBuildMessageModel(BuildMessageModel):
    @field_validator("nested", mode="before")
    def nested_validator(cls, v: Union[str, list]) -> list:
        if isinstance(v, str):
            return [i for i in v.split("/") if i if not i.startswith("$")]
        return v


class GrpcServiceOptionModel(BaseModel):
    """grpc service option"""

    name: str = Field("", description="service name")
    author: Tuple[str] = Field(default_factory=tuple, description="service author")
    tag: List[Tuple[str, str]] = Field(default_factory=list, description="service openapi tag")
    group: str = Field("", description="service pait group")
    desc: str = Field("", description="service openapi description")
    summary: str = Field("", description="service openapi summary")
    url: str = Field("", description="service url")
    enable: bool = Field(True, description="Whether to enable this service")
    http_method: str = Field("POST")
    request_message: RequestBuildMessageModel = Field(
        default_factory=RequestBuildMessageModel, description="request message"
    )
    response_message: BuildMessageModel = Field(default_factory=BuildMessageModel, description="response message")


def get_grpc_service_model_from_option_message(option_message: Message) -> List[GrpcServiceOptionModel]:
    """replace grpc service method option message to GrpcServiceOptionModel"""
    grpc_service_model_list: List[GrpcServiceOptionModel] = []
    grpc_service_option_dict: dict = {}
    for rule_filed, value in option_message.ListFields():
        key: str = rule_filed.name
        if key == "tag":
            grpc_service_option_dict[key] = [(tag.name, tag.desc) for tag in value]
        elif key == "not_enable":
            grpc_service_option_dict["enable"] = not value
        elif rule_filed.containing_oneof:
            if value.url:
                grpc_service_option_dict["url"] = value.url
            if key == "custom":
                logging.warning(f"Not support column:{key}")
            elif key != "any":
                grpc_service_option_dict["http_method"] = key
        elif key in ("body", "response_body"):
            logging.warning(f"Not support column:{key}")
        elif key == "additional_bindings":
            for item in value:
                grpc_service_model_list.extend(get_grpc_service_model_from_option_message(item))
        elif key in ("request_message", "response_message"):
            if isinstance(value, dict):
                grpc_service_option_dict[key] = value
            else:
                grpc_service_option_dict[key] = MessageToDict(value, preserving_proto_field_name=True)
        else:
            grpc_service_option_dict[key] = value

    grpc_service_model: GrpcServiceOptionModel = GrpcServiceOptionModel(**grpc_service_option_dict)
    grpc_service_model.http_method = grpc_service_model.http_method.upper()
    grpc_service_model_list.append(grpc_service_model)
    return grpc_service_model_list
