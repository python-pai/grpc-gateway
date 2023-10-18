from __future__ import annotations

from fastapi import FastAPI
from google.protobuf.json_format import MessageToDict  # type: ignore
from pait.app.any.util import sniffing_dict

from example.fastapi_example.utils import create_app
from example.starlette_example.grpc_route import add_grpc_gateway_route

sniffing_dict[FastAPI] = lambda _: "starlette"


if __name__ == "__main__":
    with create_app() as app:
        add_grpc_gateway_route(app)
