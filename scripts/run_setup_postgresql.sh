#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_setup_postgresql.sh: Setup a PostgreSQL Docker container.
#
# ------------------------------------------------------------------------------

if [ -z "${DCR_CONNECTION_PORT}" ]; then
    export DCR_CONNECTION_PORT=5432
fi

if [ -z "${DCR_CONTAINER_PORT}" ]; then
    export DCR_CONTAINER_PORT=5432
fi

if [ -z "${DCR_VERSION}" ]; then
    export DCR_VERSION=latest
fi

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "DCR - Setup a PostgreSQL Docker container."
echo "--------------------------------------------------------------------------------"
echo "CONNECTION_PORT           : ${DCR_CONNECTION_PORT}"
echo "CONTAINER_PORT            : ${DCR_CONTAINER_PORT}"
echo "VERSION                   : ${DCR_VERSION}"
echo --------------------------------------------------------------------------------

echo "Docker stop/rm dcr_db ...................................... before:"
docker ps -a
docker ps | grep "dcr_db" && docker stop dcr_db
docker ps -a | grep "dcr_db" && docker rm --force dcr_db
echo "............................................................. after:"
docker ps -a

start=$(date +%s)

# ------------------------------------------------------------------------------
# PostgreSQL                                   https://hub.docker.com/_/postgres
# ------------------------------------------------------------------------------

echo "PostgreSQL."
echo "--------------------------------------------------------------------------------"
echo "Docker create dcr_db (PostgreSQL ${DCR_VERSION})"

docker create -e        POSTGRES_DB=dcr_db_admin \
              -e        POSTGRES_HOST_AUTH_METHOD=password \
              -e        POSTGRES_PASSWORD=postgresql \
              -e        POSTGRES_USER=dcr_user_admin \
              --name    dcr_db \
              -p        "${DCR_CONNECTION_PORT}":"${DCR_CONTAINER_PORT}" \
              postgres:"${DCR_VERSION}"

echo "Docker start dcr_db (PostgreSQL ${DCR_VERSION}) ..."
if ! docker start dcr_db; then
    exit 255
fi

sleep 30

end=$(date +%s)
echo "DOCKER PostgreSQL was ready in $((end - start)) seconds"

docker ps

echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
