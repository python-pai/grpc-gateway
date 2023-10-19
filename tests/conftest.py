import asyncio
from contextlib import contextmanager
from queue import Queue
from typing import Any, Callable, Generator, List, Optional, Tuple, Union

import grpc
from pait.extra.config import apply_block_http_method_set
from pait.g import config

config.init_config(apply_func_list=[apply_block_http_method_set({"HEAD", "OPTIONS"})])


GRPC_RESPONSE = Union[grpc.Call, grpc.Future]


class ClientCallDetailsType(grpc.ClientCallDetails):
    method: str
    timeout: Optional[float]
    metadata: Optional[List[Tuple[str, Union[str, bytes]]]]
    credentials: Optional[grpc.CallCredentials]
    wait_for_ready: Optional[bool]
    compression: Optional[grpc.Compression]


class GrpcClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, queue: Queue):
        self.queue: Queue = queue

    def intercept_unary_unary(
        self,
        continuation: Callable,
        call_details: ClientCallDetailsType,
        request: Any,
    ) -> GRPC_RESPONSE:
        self.queue.put(request)
        return continuation(call_details, request)


class AioGrpcClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, queue: Queue):
        self.queue: Queue = queue

    def intercept_unary_unary(
        self,
        continuation: Callable,
        call_details: ClientCallDetailsType,
        request: Any,
    ) -> GRPC_RESPONSE:
        self.queue.put(request)
        return continuation(call_details, request)


@contextmanager
def fixture_loop(mock_close_loop: bool = False) -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    def _mock(_loop: Optional[asyncio.AbstractEventLoop] = None) -> Optional[asyncio.AbstractEventLoop]:
        return loop

    if mock_close_loop:
        close_loop = loop.close
    set_event_loop = asyncio.set_event_loop
    new_event_loop = asyncio.new_event_loop
    try:
        asyncio.set_event_loop = _mock  # type: ignore
        asyncio.new_event_loop = _mock  # type: ignore
        if mock_close_loop:
            loop.close = lambda: None  # type: ignore
        yield loop
    finally:
        asyncio.set_event_loop = set_event_loop
        asyncio.new_event_loop = new_event_loop
        if mock_close_loop:
            loop.close = close_loop  # type: ignore
    return None
