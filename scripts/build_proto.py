"""Generates protocol messages and gRPC stubs."""

from grpc_tools import protoc
from subprocess import check_output
from os import chdir, mkdir

base_dir = str(check_output(['git', 'rev-parse', '--show-toplevel']))[2:-3]
chdir(base_dir)
mkdir(base_dir + '/src/protobufgen')

protoc.main(
    (
        '',
        '-I./api',
        '--python_out=./src/protobufgen',
        '--grpc_python_out=./src/protobufgen',
        './api/soccer3d.proto',
    )
)
