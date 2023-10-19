import pytest
from pait import field

from grpc_gateway.desc_template import DescTemplate


def test_field_template() -> None:
    desc_template = DescTemplate({}, comment_prefix="grpc-gateway")
    assert field.Query == desc_template.handle_template_var("grpc-gateway@field|Query")
    with pytest.raises(ValueError):
        desc_template.handle_template_var("grpc-gateway@field|None")
