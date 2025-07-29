import os
import re
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from grpc_tools import protoc

class build_proto(_build_py):
    def run(self):
        proto_root = os.path.abspath("proto")
        out_dir    = os.path.abspath("src/common_grpc")
        os.makedirs(out_dir, exist_ok=True)

        for root, _, files in os.walk(proto_root):
            for fn in files:
                if fn.endswith(".proto"):
                    full = os.path.join(root, fn)
                    protoc.main([
                        "grpc_tools.protoc",
                        f"-I{proto_root}",
                        f"--python_out={out_dir}",
                        f"--grpc_python_out={out_dir}",
                        full,
                    ])

        for root, _, files in os.walk(out_dir):
            for fn in files:
                if not fn.endswith(".py"):
                    continue
                file_path = os.path.join(root, fn)
                text = open(file_path, encoding="utf-8").read()

                text = re.sub(
                    r"^from\s+auth_service\s+import\s+auth_pb2\s+as\s+(\S+)",
                    r"from common_grpc.auth_service import auth_pb2 as \1",
                    text, flags=re.M
                )
                text = re.sub(
                    r"^import\s+auth_service\.auth_pb2\s+as\s+(\S+)",
                    r"import common_grpc.auth_service.auth_pb2 as \1",
                    text, flags=re.M
                )

                text = re.sub(
                    r"^from\s+exchanger_cabinet\s+import\s+courses_pb2\s+as\s+(\S+)",
                    r"from common_grpc.exchanger_cabinet import courses_pb2 as \1",
                    text, flags=re.M
                )
                text = re.sub(
                    r"^import\s+exchanger_cabinet\.courses_pb2\s+as\s+(\S+)",
                    r"import common_grpc.exchanger_cabinet.courses_pb2 as \1",
                    text, flags=re.M
                )

                text = re.sub(
                    r"^from\s+common\s+import\s+common_pb2\s+as\s+(\S+)",
                    r"from common_grpc.common import common_pb2 as \1",
                    text, flags=re.M
                )
                text = re.sub(
                    r"^import\s+common\.common_pb2\s+as\s+(\S+)",
                    r"import common_grpc.common.common_pb2 as \1",
                    text, flags=re.M
                )

                text = re.sub(
                    r"(^from\s+)auth_service(\.[^ ]+)",
                    r"\1common_grpc.auth_service\2",
                    text, flags=re.M
                )
                text = re.sub(
                    r"(^import\s+)auth_service(\.[^ ]+)",
                    r"\1common_grpc.auth_service\2",
                    text, flags=re.M
                )
                text = re.sub(
                    r"(^from\s+)exchanger_cabinet(\.[^ ]+)",
                    r"\1common_grpc.exchanger_cabinet\2",
                    text, flags=re.M
                )
                text = re.sub(
                    r"(^import\s+)exchanger_cabinet(\.[^ ]+)",
                    r"\1common_grpc.exchanger_cabinet\2",
                    text, flags=re.M
                )
                text = re.sub(
                    r"(^from\s+)course_parser(\.[^ ]+)",
                    r"\1common_grpc.course_parser\2",
                    text, flags=re.M
                )
                text = re.sub(
                    r"(^import\s+)course_parser(\.[^ ]+)",
                    r"\1common_grpc.course_parser\2",
                    text, flags=re.M
                )

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)

        super().run()

setup(
    name="coursehunt-grpc",
    version="0.1.4",
    description="gRPC contracts and Python stubs for Coursehunt",
    author="Dmitriy Pelevin",
    author_email="dmitriy.pelevin@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio>=1.54.0",
        "protobuf>=4.0.0",
    ],
    cmdclass={"build_py": build_proto},
    include_package_data=True,
)
