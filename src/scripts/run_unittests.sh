#!/bin/sh

start=$WORKSPACE/tests/tests_web_platform

python -m unittest discover -s $start -p "*_test.py"
