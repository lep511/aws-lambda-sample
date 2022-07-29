#!/bin/bash
set -eo pipefail
rm -rf package
if type python3.9 >/dev/null 2>&1 
then 
    python3.9 -m pip install --upgrade pip
    python3.9 -m pip install -r requirements.txt -t package/python
else
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt -t package/python
fi
