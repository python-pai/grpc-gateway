import sys
from pathlib import Path
from typing import Any, Dict, List

import grpc

from grpc_gateway.model import GrpcServiceOptionModel, get_grpc_service_model_from_option_message
from grpc_gateway.protobuf_types import ServiceDescriptor

sys.path.append(str(Path(__file__).parent.absolute()))

gen_demo_module = grpc.protos("demo.proto")
gen_demo_services = grpc.services("demo.proto")


def get_grpc_service_model_option(module: Any) -> Dict[str, List[GrpcServiceOptionModel]]:
    server_list: List[ServiceDescriptor] = module.DESCRIPTOR.services_by_name.values()  # type: ignore
    server_list_dict: Dict[str, List[GrpcServiceOptionModel]] = {}
    for server_descriptor in server_list:
        for method in server_descriptor.methods:
            if not method.GetOptions().ListFields():
                continue
            for field, option_message in method.GetOptions().ListFields():
                if not field.full_name.endswith("api.http"):
                    continue
                server_list_dict[method.name] = get_grpc_service_model_from_option_message(option_message)
    return server_list_dict
