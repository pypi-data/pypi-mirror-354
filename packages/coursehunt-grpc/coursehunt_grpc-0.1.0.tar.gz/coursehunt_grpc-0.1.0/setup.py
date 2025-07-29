import os
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
        super().run()

setup(
    cmdclass = {"build_py": build_proto},
    packages  = find_packages(where="src"),
    package_dir = {"": "src"},
)
