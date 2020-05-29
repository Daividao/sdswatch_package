#!/usr/bin/env bash

# clean up old sdswatch-client in case it's running
docker stop sdswatch-client
docker rm sdswatch-client
export HOST_UID=$(id -u)
export HOST_GID=$(id -g)
export HOST=$(curl ifconfig.me)
docker-compose build
docker-compose up

