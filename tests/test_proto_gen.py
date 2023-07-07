import filecmp
import sys

project_path: str = ""

for path in set(sys.path):
    if path.endswith("grpc-gateway"):
        project_path = path


class TestProtoGen:
    """Check whether the PB file in pkg is consistent with the PB file in the example"""

    def test_api_proto(self) -> None:
        assert filecmp.cmp(
            project_path + "/example/grpc_common/example_proto_by_option/common/api.proto",
            project_path + "/grpc_gateway/proto/api.proto",
        )
