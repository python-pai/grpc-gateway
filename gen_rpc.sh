#!/bin/bash
# gen python protos code path
target_p='grpc_gateway/proto'
# project proto path
source_p='grpc_gateway/proto'

poetry run python -m grpc_tools.protoc \
  --mypy_grpc_out=./$source_p \
  --mypy_out=./$source_p \
  --python_out=./$source_p \
  --grpc_python_out=./$source_p \
  -I $source_p $(find ./$source_p -name '*.proto')
