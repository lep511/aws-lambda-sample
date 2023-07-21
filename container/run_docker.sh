#!/bin/bash
if [ -z $1 ]; then
    echo "DOCKER_IMAGE is not set"
    echo "Using default docker image name: test-image"
    export docker_image=test-image
else
    export docker_image=$4
fi

docker build -t $1 .
echo "=================="
echo "  "
echo "Run in another window: curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'"
docker run -p 9000:8080 $1
