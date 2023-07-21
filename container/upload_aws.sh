#!/bin/bash

#Check aws account id
if [ -z $1 ]; then
    echo "ACCOUNT_ID is not set"
    exit 1
else
    export ACCOUNT_ID=$1
fi

# Check aws region
if [ -z $2 ]; then
    echo "AWS_REGION is not set"
    echo "Using default region: us-east-1"
    export AWS_REGION=us-east-1
else
    export AWS_REGION=$2
fi

# Check repository name
if [ -z $3 ]; then
    echo "REPOSITORY_NAME is not set"
    echo "Using default repository name: test-repo"
    export repository=test-repo
else
    export repository=$3
fi

# Check docker image name
if [ -z $4 ]; then
    echo "DOCKER_IMAGE is not set"
    echo "Using default docker image name: test-image"
    export docker_image=test-image
else
    export docker_image=$4
fi

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr create-repository --repository-name $repository --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
docker tag $docker_image:test $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$repository:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$repository:latest
