#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_setup_postgresql.sh: Setup a PostgreSQL Docker container.
#
# ------------------------------------------------------------------------------

export DCR_ENVIRONMENT_TYPE_DEFAULT=dev

if [ -z "${DCR_CONTAINER_PORT}" ]; then
    export DCR_CONTAINER_PORT=5432
fi

if [ -z "${DCR_VERSION}" ]; then
    export DCR_VERSION=latest
fi

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "dev  - Environment Development."
    echo "prod - Environment Production."
    echo "test - Environment Test."
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired environment [default: ${DCR_ENVIRONMENT_TYPE_DEFAULT}] " DCR_ENVIRONMENT_TYPE
    export DCR_ENVIRONMENT_TYPE=${DCR_ENVIRONMENT_TYPE:-$DCR_ENVIRONMENT_TYPE_DEFAULT}
else
    export DCR_ENVIRONMENT_TYPE=$1
fi

if [ -z "${DCR_CONNECTION_PORT}" ]; then
    if [ "${DCR_ENVIRONMENT_TYPE}" = "dev" ]; then
        export DCR_CONNECTION_PORT=5432
    fi
    if [ "${DCR_ENVIRONMENT_TYPE}" = "prod" ]; then
        export DCR_CONNECTION_PORT=5433
    fi
    if [ "${DCR_ENVIRONMENT_TYPE}" = "test" ]; then
        export DCR_CONNECTION_PORT=5434
    fi
fi

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "DCR - Setup a PostgreSQL Docker container."
echo "--------------------------------------------------------------------------------"
echo "CONNECTION_PORT    : ${DCR_CONNECTION_PORT}"
echo "CONTAINER_PORT     : ${DCR_CONTAINER_PORT}"
echo "ENVIRONMENT        : ${DCR_ENVIRONMENT_TYPE}"
echo "POSTGRESQL VERSION : ${DCR_VERSION}"
echo --------------------------------------------------------------------------------

echo "Docker stop/rm dcr_db_${DCR_ENVIRONMENT_TYPE} ...................................... before:"
docker ps -a
docker ps | grep "dcr_db_${DCR_ENVIRONMENT_TYPE}" && docker stop dcr_db_${DCR_ENVIRONMENT_TYPE}
docker ps -a | grep "dcr_db_${DCR_ENVIRONMENT_TYPE}" && docker rm --force dcr_db_${DCR_ENVIRONMENT_TYPE}
echo "............................................................. after:"
docker ps -a

start=$(date +%s)

# ------------------------------------------------------------------------------
# PostgreSQL                                   https://hub.docker.com/_/postgres
# ------------------------------------------------------------------------------

echo "PostgreSQL."
echo "--------------------------------------------------------------------------------"
echo "Docker create dcr_db_${DCR_ENVIRONMENT_TYPE} (PostgreSQL ${DCR_VERSION})"

docker create -e        POSTGRES_DB=dcr_db_${DCR_ENVIRONMENT_TYPE}_admin \
              -e        POSTGRES_HOST_AUTH_METHOD=password \
              -e        POSTGRES_PASSWORD=postgresql \
              -e        POSTGRES_USER=dcr_user_admin \
              --name    dcr_db_${DCR_ENVIRONMENT_TYPE} \
              -p        "${DCR_CONNECTION_PORT}":"${DCR_CONTAINER_PORT}" \
              postgres:"${DCR_VERSION}"

echo "Docker start dcr_db_${DCR_ENVIRONMENT_TYPE} (PostgreSQL ${DCR_VERSION}) ..."
if ! docker start dcr_db_${DCR_ENVIRONMENT_TYPE}; then
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
