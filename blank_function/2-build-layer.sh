#!/bin/bash
set -eo pipefail
rm -rf package
cd function
python3.9 -m pip install -r requirements.txt -t ../package/python