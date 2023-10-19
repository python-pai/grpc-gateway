import inspect
from typing import Any

from pait import field as pait_field
from protobuf_to_pydantic.gen_model import DescTemplate as _DescTemplate

__all__ = ["DescTemplate"]


class DescTemplate(_DescTemplate):
    def template_field(self, field: str) -> Any:
        """
        Desc:
            Support Pait field
        e.g:
            protobuf content:
                message GetBookRequest {
                  string isbn = 1 [(p2p_validate.rules).string.field = "grpc-gateway@field|Query"];
                  string not_use_field1 = 2;
                  string not_use_field2 = 3;
                }
            gen Message model:
                from pait.field import Query

                class GetBookRequest(BaseModel):
                    isbn: str = Query.i()
                    not_use_field1: str
                    not_use_field2: str

        :param field: field class name
        :return: field class
        """
        field_class: Any = getattr(pait_field, field, None)
        if not inspect.isclass(field_class) or not issubclass(field_class, pait_field.BaseRequestResourceField):
            raise ValueError(f"{field} is not a valid field")
        return field_class
