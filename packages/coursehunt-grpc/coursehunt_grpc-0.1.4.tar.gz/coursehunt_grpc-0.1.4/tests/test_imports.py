import pytest
import importlib

MODULES = [
    "common_grpc.auth_service.auth_pb2",
    "common_grpc.auth_service.auth_pb2_grpc",
    "common_grpc.course_parser.courses_pb2",
    "common_grpc.course_parser.courses_pb2_grpc",
    "common_grpc.exchanger_cabinet.auth_pb2",
    "common_grpc.exchanger_cabinet.auth_pb2_grpc",
    "common_grpc.exchanger_cabinet.courses_pb2",
    "common_grpc.exchanger_cabinet.courses_pb2_grpc",
]

@pytest.mark.parametrize("module_name", MODULES)
def test_module_import(module_name):
    importlib.import_module(module_name)
