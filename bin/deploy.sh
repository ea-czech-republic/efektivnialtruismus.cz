#!/usr/bin/env sh
set -ex

[[ -z $IMAGE_TAG ]] && echo "You must pass IMAGE_TAG var" && exit 1
[[ -z $IMAGE_TAG ]] && echo "You must pass IMAGE_TAG var" && exit 1

# this was done by git clone https://github.com/ea-czech-republic/efektivnialtruismus.cz.git
cd /var/server/efektivnialtruismus.cz
git pull

# because docker-compose does not have credentials from host
docker pull gcr.io/efektivni-altruismus/effective-thesis:${IMAGE_TAG}

docker run --rm \
    -e IMAGE_TAG=$IMAGE_TAG \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.24.0 \
    -f docker-compose.yaml \
    -f dc-.yaml \
    up \
    -d \
    --force-recreate
