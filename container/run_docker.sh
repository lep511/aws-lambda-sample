#!/bin/bash
docker build -t $1 .
echo Run in another window: curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
docker run -p 9000:8080 $1
