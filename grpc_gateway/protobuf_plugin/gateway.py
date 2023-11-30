from typing import Any, List, Optional, Union

import grpc
from pait.app.any import add_multi_simple_route as _add_multi_simple_route
from grpc_gateway.base_gateway import BaseGrpcGatewayRoute, BaseGrpcGatewayRouteConfig
from pait.util import get_real_annotation

StaticGrpcGatewayRouteConfig = BaseGrpcGatewayRouteConfig


class BaseStaticGrpcGatewayRoute(BaseGrpcGatewayRoute[StaticGrpcGatewayRouteConfig]):
    add_multi_simple_route: staticmethod = staticmethod(_add_multi_simple_route)
    stub_str_list: List[str]

    def __init__(
        self,
        app: Any,
        is_async: bool,
        channel: Union[grpc.Channel, grpc.aio.Channel, None] = None,
        config: Optional[BaseGrpcGatewayRouteConfig] = None
    ):
        """
        :param app: Instance object of the web framework
        :param channel: grpc Channel
        """
        super().__init__(app, config=config)
        self.is_async: bool = is_async
        if channel:
            self.reinit_channel(channel)
        self.gen_route()

    def gen_route(self) -> None:
        raise NotImplementedError

    def reinit_channel(
        self, channel: Union[grpc.Channel, grpc.aio.Channel], auto_close: bool = False
    ) -> Union[grpc.Channel, grpc.aio.Channel, None]:
        for stub_str in self.stub_str_list:
            setattr(self, stub_str, get_real_annotation(self.__annotations__[stub_str], self)(channel))
        return super().reinit_channel(channel, auto_close)
