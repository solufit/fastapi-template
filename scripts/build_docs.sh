#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR

cd ..
pip install -r ./docs/requirements.txt
sphinx-apidoc -f -o ./docs/source src tests

cp -r docs /tmp/docs

cd /tmp/docs
mkdir /tmp/output

sphinx-build -M html /tmp/docs/source /tmp/output