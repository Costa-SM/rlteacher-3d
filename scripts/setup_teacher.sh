#!/bin/bash

pushd $(git rev-parse --show-toplevel) &> /dev/null

echo "Creating Python Virtual Environment and installing requirements..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

PROTO_DIR=src/protobuf

if [ -d "$PROTO_DIR" ];
then
    echo "Removing old protobuf files..."
    rm $PROTO_DIR -rf
fi

echo "Generating protobuf files..."
python ./scripts/build_proto.py

popd &> /dev/null
