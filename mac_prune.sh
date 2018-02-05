#!/bin/sh +x

DOCKER=$(which docker)

DOCKER container prune -f
DOCKER network prune -f
DOCKER volume prune -f
DOCKER image prune -f

