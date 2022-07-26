#!/bin/bash
set -eo pipefail
rm -rf package
python3.9 -m pip install -r requirements.txt -t package/python