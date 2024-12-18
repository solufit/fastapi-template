#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR

cd ..
pip install -r ./docs/requirements.txt
sphinx-apidoc -f -o ./docs/source src tests

cd docs

make html
