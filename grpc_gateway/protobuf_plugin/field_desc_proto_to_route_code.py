import logging
from dataclasses import asdict
from textwrap import dedent
from typing import TYPE_CHECKING, List, Tuple

from jinja2 import Template
from mypy_protobuf.main import Descriptors
from grpc_gateway.__version__ import __version__
from grpc_gateway.model import GrpcServiceOptionModel, get_grpc_service_model_from_option_message
from grpc_gateway.protobuf_plugin.model import GrpcTemplateVarModel
from protobuf_to_pydantic.gen_code import BaseP2C
from protobuf_to_pydantic.gen_model import DescTemplate
from protobuf_to_pydantic.grpc_types import FileDescriptorProto

if TYPE_CHECKING:
    from grpc_gateway.protobuf_plugin.config import ConfigModel

logger: logging.Logger = logging.getLogger(__name__)


class FileDescriptorProtoToRouteCode(BaseP2C):
    head_content: str = (
        "# This is an automatically generated file, please do not change\n"
        f"# gen by grpc-gateway[{__version__}](https://github.com/python-pai/grpc-gateway)\n"
    )
    indent: int = 4
    attr_prefix: str = "gateway_attr"
    gateway_name: str = "StaticGrpcGatewayRoute"
    route_func_jinja_template_str: str = dedent(
        """
    {% if  request_message_model in ("Empty",) %}
    {{ 'async def' if is_async else 'def' }} {{func_name}}() -> Any:
    {% else %}
    {{ 'async def' if is_async else 'def' }} {{func_name}}(
        request_pydantic_model: {{request_message_model_name}}
    ) -> Any:
    {% endif %}
        gateway: "{{gateway_name}}" = pait_context.get().app_helper.get_attributes(
            "{{attr_prefix}}_{{filename}}_gateway"
        )
    {% if  request_message_model in ("Empty", ) %}
        request_msg: {{request_message_name}} = {{request_message_name}}()
    {% else %}
        request_msg: {{request_message_name}} = gateway.msg_from_dict_handle(
            {{request_message_name}},
        {% if pydantic_is_v1 %}
            request_pydantic_model.dict(),
        {% else %}
            request_pydantic_model.model_dump(),
        {% endif %}
            {{gen_code._get_value_code(grpc_service_option_model.request_message.nested)}}
        )
    {% endif %}
    {% if is_async %}
        gateway.check_event_loop(gateway.{{stub_service_name}}.{{method}})
        grpc_msg: {{response_message_name}} = await gateway.{{stub_service_name}}.{{method}}(
            request_msg
        )
    {% else %}
        grpc_msg: {{response_message_name}} = gateway.{{stub_service_name}}.{{method}}(request_msg)
    {% endif %}
        return gateway.msg_to_dict_handle(
            grpc_msg,
            {{gen_code._get_value_code(grpc_service_option_model.response_message.exclude_column_name)}},
            {{gen_code._get_value_code(grpc_service_option_model.response_message.nested)}}
        )
        """
    )

    response_jinja_template_str: str = dedent(
        """
    class {{response_class_name}}(JsonResponseModel):
        {% if response_message_model_name == "Empty" %}
        description: str = (
            {{gen_code._get_value_code(gen_code.config.empty_type)}}.__doc__ or ""
            if {{gen_code._get_value_code(gen_code.config.empty_type)}}.__module__ != "builtins" else ""
        )
        response_data: {{
            gen_code._get_value_code(gen_code.config.empty_type)
        }} = {{gen_code._get_value_code(gen_code.config.empty_type)}}
        {% else %}
        description: str = (
            {{response_message_model_name}}.__doc__ or ""
            if {{response_message_model_name}}.__module__ != "builtins" else ""
        )
        response_data: Type[BaseModel] = {{response_message_model_name}}
        {% endif %}
    """
    )

    def __init__(self, fd: FileDescriptorProto, descriptors: Descriptors, config: "ConfigModel"):
        config = config.copy(deep=True)
        super().__init__(
            customer_import_set=config.customer_import_set,
            customer_deque=config.customer_deque,
            module_path=config.module_path,
            code_indent=config.code_indent,
        )
        self.config: "ConfigModel" = config
        self._fd: FileDescriptorProto = fd
        self._descriptors: Descriptors = descriptors
        self._desc_template: DescTemplate = config.desc_template_instance

        self._parse_field_descriptor()

    def get_route_code(self, grpc_model: GrpcTemplateVarModel, template_dict: dict) -> str:
        """Can customize the template that generates the route according to different methods"""
        return Template(self.route_func_jinja_template_str, trim_blocks=True, lstrip_blocks=True).render(
            **template_dict
        )

    def get_response_code(self, grpc_model: GrpcTemplateVarModel, template_dict: dict) -> str:
        """Can customize the template that generates the response according to different methods"""
        return Template(self.response_jinja_template_str, trim_blocks=True, lstrip_blocks=True).render(**template_dict)

    def get_pait_code(self, tab_str: str, pait_name: str, grpc_model: GrpcTemplateVarModel) -> str:
        option_model = grpc_model.grpc_service_option_model
        # can't change tab_str, pait_name value
        tag_str_list: List[str] = [
            f'Tag("{tag}", "{desc}")'
            for tag, desc in option_model.tag + [("grpc" + "-" + grpc_model.grpc_method_url.split("/")[1].split(".")[0], "")]
        ]
        tag_str_list.append("self._grpc_tag")
        name = '"' + option_model.name + '"' if option_model.name else None
        desc = '"' + option_model.desc + '"' if option_model.desc else None
        summary = '"' + option_model.summary + '"' if option_model.summary else None
        return (
            f"{tab_str * 2}{pait_name}: Pait = self._pait.create_sub_pait(\n"
            f"{tab_str * 3}append_author={self._get_value_code(option_model.author or None)},\n"
            f'{tab_str * 3}name={name},\n'
            f"{tab_str * 3}group={self._get_value_code(option_model.group or None)},\n"
            f"{tab_str * 3}append_tag=({', '.join(tag_str_list) if tag_str_list else None},),\n"
            f'{tab_str * 3}desc={desc},\n'
            f'{tab_str * 3}summary={summary},\n'
            f"{tab_str * 3}default_field_class="
            f'{"field.Query" if grpc_model.grpc_service_option_model.http_method == "GET" else "field.Json"},\n'
            f"{tab_str * 3}response_model_list=[{grpc_model.response_class_name}] + response_model_list,\n"
            f"{tab_str * 2})"
        )

    def extra_data_by_fd(
        self, model_module_name: str, message_module_name: str, stub_module_name: str
    ) -> Tuple[List[GrpcTemplateVarModel], List[str]]:
        service_name_list: list = []
        grpc_template_var_model_list: List[GrpcTemplateVarModel] = []
        for service in self._fd.service:
            for method in service.method:
                func_name: str = f"{method.name}_route"
                service_name_list.append(service.name)
                service_model_list: List[GrpcServiceOptionModel] = []
                for field, option_message in method.options.ListFields():
                    if not field.full_name.endswith("api.http"):
                        continue
                    service_model_list.extend(get_grpc_service_model_from_option_message(option_message))
                input_type_name = method.input_type.split(".")[-1]
                output_type_name = method.output_type.split(".")[-1]
                # TODO A more elegant implementation of the google.protocol type
                if "Empty" in (input_type_name, output_type_name):
                    self._add_import_code("google.protobuf.empty_pb2", "Empty")
                grpc_method_url: str = f"/{self._fd.package}-{service.name}/{method.name}"
                if not service_model_list:
                    service_model_list.append(GrpcServiceOptionModel(url=grpc_method_url))
                for model_index, grpc_service_option_model in enumerate(service_model_list):
                    if not grpc_service_option_model.url:
                        grpc_service_option_model.url = grpc_method_url
                    request_message_model_name = f"{model_module_name}.{input_type_name}"
                    response_message_model_name = f"{model_module_name}.{output_type_name}"

                    ###################
                    # rebuild Message #
                    ###################
                    # Generating code directly would be very cumbersome, so here is a simplification
                    r_message_model_name_list = [request_message_model_name, response_message_model_name]
                    for request_build_message, i_o_type_name in [
                        (grpc_service_option_model.request_message, input_type_name),
                        (grpc_service_option_model.response_message, output_type_name)
                    ]:
                        if not(
                            (
                                request_build_message.exclude_column_name or request_build_message.nested
                            ) and i_o_type_name != "Empty"
                        ):
                            continue
                        exclude_column_name_str = self._get_value_code(request_build_message.exclude_column_name)
                        nested_str = self._get_value_code(request_build_message.nested, sort=False)
                        r_message_model_name = f"{i_o_type_name}{''.join([i.title() for i in func_name.split('_')])}"
                        if i_o_type_name == input_type_name:
                            r_message_model_name_list[0] = r_message_model_name
                        else:
                            r_message_model_name_list[1] = r_message_model_name
                        self._add_import_code(f".{model_module_name}", i_o_type_name, f" as {r_message_model_name}")
                        self._add_import_code("grpc_gateway.rebuild_message", "rebuild_message_type")
                        self._content_deque.append(
                            dedent(
                                f"""
                                {r_message_model_name} = rebuild_message_type(  # type: ignore[misc]
                                    {r_message_model_name},
                                    "{func_name}",
                                    exclude_column_name={exclude_column_name_str},
                                    nested={nested_str},
                                )
                                """
                            )
                        )
                    grpc_template_var_model_list.append(
                        GrpcTemplateVarModel(
                            index=model_index,
                            attr_prefix=self.attr_prefix,
                            filename=self._fd.name,
                            gateway_name=self.gateway_name,
                            method=method.name,
                            func_name=func_name,
                            input_type_name=input_type_name,
                            output_type_name=output_type_name,
                            request_message_model_name=r_message_model_name_list[0]
                            if input_type_name not in ("Empty",)
                            else input_type_name,
                            response_message_model_name=r_message_model_name_list[1]
                            if output_type_name not in ("Empty",)
                            else output_type_name,
                            request_message_name=f"{message_module_name}.{input_type_name}"
                            if input_type_name not in ("Empty",)
                            else input_type_name,
                            response_message_name=f"{message_module_name}.{output_type_name}"
                            if output_type_name not in ("Empty",)
                            else output_type_name,
                            stub_service_name=f"{service.name}_stub",
                            service_name=service.name,
                            model_module_name=model_module_name,
                            message_module_name=message_module_name,
                            stub_module_name=stub_module_name,
                            package=self._fd.package,
                            grpc_method_url=grpc_method_url,
                            grpc_service_option_model=grpc_service_option_model,
                            grpc_descriptor_method=method,
                            grpc_descriptor_service=service,
                            response_class_name=(
                                self._fd.package.title().replace("_", "") + output_type_name + "JsonResponseModel"
                            ),
                            gen_code=self,
                        )
                    )
        return grpc_template_var_model_list, service_name_list

    def _parse_field_descriptor(self) -> None:
        tab_str: str = self.indent * " "
        model_module_name = self._fd.name.split("/")[-1].replace(".proto", self.config.file_name_suffix)
        message_module_name = self._fd.name.split("/")[-1].replace(".proto", "_pb2")
        stub_module_name = self._fd.name.split("/")[-1].replace(".proto", "_pb2_grpc")

        self._add_import_code("pait", "field")
        self._add_import_code("pait.app.any", "SimpleRoute")
        self._add_import_code("pait.app.any", "set_app_attribute")
        self._add_import_code("pait.core", "Pait")
        self._add_import_code("pait.g", "pait_context")
        self._add_import_code("grpc_gateway.protobuf_plugin.gateway", "BaseStaticGrpcGatewayRoute")
        self._add_import_code("pait.model.tag", "Tag")
        self._add_import_code("pait.model.response", "BaseResponseModel")
        self._add_import_code("pait.model.response", "JsonResponseModel")
        self._add_import_code("pydantic", "BaseModel")
        self._add_import_code("typing", "Any")
        self._add_import_code("typing", "Callable")
        self._add_import_code("typing", "List")
        self._add_import_code("typing", "Type")

        self._add_import_code(".", model_module_name)
        self._add_import_code(".", message_module_name)
        self._add_import_code(".", stub_module_name)

        grpc_template_var_model_list, service_name_list = self.extra_data_by_fd(
            model_module_name, message_module_name, stub_module_name
        )
        #######################################################################
        # Refine the information through the GRPC model and generate the code #
        #######################################################################
        route_code_str_list: List[str] = []
        response_code_str_list: List[str] = []

        simple_route_str_list: List[str] = []
        wrapper_route_str_list = []

        for grpc_template_var_model in grpc_template_var_model_list:
            # Specifies that the data is not parsed and skipped
            grpc_service_option_model = grpc_template_var_model.grpc_service_option_model
            if not grpc_service_option_model.enable:
                continue

            if grpc_template_var_model.index == 0:
                # The response model code only needs to be generated once
                template_dict: dict = asdict(grpc_template_var_model)
                response_code_str_list.append(self.get_response_code(grpc_template_var_model, template_dict) + "\n")

            base_func_name: str = grpc_template_var_model.func_name
            if grpc_template_var_model.index:
                base_func_name = base_func_name + "_" + str(grpc_template_var_model.index)
            pait_name: str = base_func_name + "_pait"
            # gen create pait instance code
            wrapper_route_str_list.append(self.get_pait_code(tab_str, pait_name, grpc_template_var_model))

            for is_async in [True, False]:
                if grpc_template_var_model.index == 0:
                    # The routing function only needs to be generated once
                    template_dict = asdict(grpc_template_var_model)
                    template_dict["is_async"] = is_async
                    if is_async:
                        template_dict["func_name"] = "async_" + template_dict["func_name"]
                    route_code_str_list.append(self.get_route_code(grpc_template_var_model, template_dict) + "\n")

                # gen sub pait instance code
                func_name = grpc_template_var_model.func_name
                if is_async:
                    func_name = "async_" + func_name
                real_func_name: str = "pait_" + func_name
                if grpc_template_var_model.index:
                    real_func_name += "_" + str(grpc_template_var_model.index)
                wrapper_route_str_list.append(
                    f'{tab_str * 2}{real_func_name} = {pait_name}(feature_code="{grpc_template_var_model.index}")({func_name})'
                )

                if grpc_template_var_model.index:
                    wrapper_route_str_list.append(
                        f'{tab_str * 2}{real_func_name}.__name__ = "{real_func_name}"\n'
                        f"{tab_str * 2}{real_func_name}.__qualname__ = "
                        f'{real_func_name}.__qualname__.replace("{func_name}", "{real_func_name}")'
                    )
            simple_route_str_list.append(
                f"{tab_str * 3}SimpleRoute(\n"
                f'{tab_str * 4}url="{grpc_service_option_model.url}", \n'
                f'{tab_str * 4}methods=["{grpc_service_option_model.http_method}"], \n'
                f"{tab_str * 4}route=pait_async_{base_func_name}"
                f" if self.is_async else pait_{base_func_name}\n"
                f"{tab_str * 3})"
            )

        class_stub_str: str = ""
        stub_service_name_list: List[str] = []
        for service_name in set(service_name_list):
            stub_service_name: str = f"{service_name}_stub"
            stub_service_name_list.append(stub_service_name)
            class_stub_str += f"{tab_str * 1}{stub_service_name}: {stub_module_name}.{service_name}Stub\n"

        class_stub_str += (
            f"{tab_str * 1}stub_str_list: List[str] = {self._get_value_code(stub_service_name_list, sort=False)}\n"
        )
        gateway_class_str: str = (
            "\n"
            f"class {self.gateway_name}(BaseStaticGrpcGatewayRoute):\n"
            f"{class_stub_str}\n"
            f"{tab_str * 1}def gen_route(self) -> None:\n"
            f'{tab_str * 2}set_app_attribute(self.app, "{self.attr_prefix}_{self._fd.name}_gateway", self)\n'
            f"{tab_str * 2}# The response model generated based on Protocol is important and needs to be put first\n"
            f"{tab_str * 2}response_model_list: List[Type[BaseResponseModel]] = self._pait.response_model_list or []\n"
            f"{chr(10).join(wrapper_route_str_list) if wrapper_route_str_list else ''}\n"
            f"{tab_str * 2}self._add_multi_simple_route(\n"
            f"{tab_str * 3}self.app,\n"
            f"{(',' + chr(10)).join(simple_route_str_list) + ',' if simple_route_str_list else ''}\n"
            f"{tab_str * 3}prefix=self.config.prefix,\n"
            f"{tab_str * 3}title=self.config.title,\n"
            f"{tab_str * 3}**self._add_multi_simple_route_kwargs \n"
            f"{tab_str * 2})\n"
        )
        logger.debug(gateway_class_str)
        for response_code_str in response_code_str_list:
            self._content_deque.append(response_code_str)
        for route_code_str in route_code_str_list:
            self._content_deque.append(route_code_str)
        self._content_deque.append(gateway_class_str)
