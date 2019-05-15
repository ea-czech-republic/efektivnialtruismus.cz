#!/usr/bin/env sh
set -ex

[[ -z $IMAGE_TAG ]] && echo "You must pass IMAGE_TAG var" && exit 1

cd /var/server/efektivnialtruismus.cz
git pull
docker run --rm \
    -e IMAGE_TAG=$IMAGE_TAG \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.24.0 \
    -f docker-compose.yaml \
    -f docker-compose-production.yaml \
    up \
    --force-recreate \
    app