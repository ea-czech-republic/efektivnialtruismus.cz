#!/usr/bin/env sh
set -ex

[[ -z $IMAGE_TAG ]] && echo "You must pass IMAGE_TAG var" && exit 1
[[ -z ENVIRONMENT ]] && echo "You must pass ENVIRONMENT var which corresponds to a branch" && exit 1

if [ "$ENVIRONMENT" = "beta" ]; then
    export ENV_PREFIX="beta."
elif [ "$ENVIRONMENT" = "master" ]; then
    export ENV_PREFIX=""
else
    echo "Unknown env"
    exit 1
fi

# this was done by git clone https://github.com/ea-czech-republic/efektivnialtruismus.cz.git
cd /var/server/efektivnialtruismus.cz
git checkout $ENVIRONMENT
git pull

# because docker-compose does not have credentials from host
docker pull czea/effective-thesis:${IMAGE_TAG}

docker run --rm \
    -e IMAGE_TAG=$IMAGE_TAG \
    -e ENVIRONMENT=$ENVIRONMENT \
    -e ENV_PREFIX=$ENV_PREFIX \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.24.0 \
    -f docker-compose.yaml \
    -f dc-deploy.yaml \
    up \
    -d \
    --force-recreate
