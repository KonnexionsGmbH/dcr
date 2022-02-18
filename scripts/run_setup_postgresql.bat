@echo off

rem ------------------------------------------------------------------------------
rem
rem run_setup_postgresql.bat: Setup a PostgreSQL Docker container.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

if ["%DCR_CONNECTION_PORT%"] EQU [""] (
    set DCR_CONNECTION_PORT=5432
)

if ["%DCR_CONTAINER_PORT%"] EQU [""] (
    set DCR_CONTAINER_PORT=5432
)

if ["%DCR_VERSION%"] EQU [""] (
    set DCR_VERSION=latest
)

echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo DCR - Setup a PostgreSQL Docker container.
echo --------------------------------------------------------------------------------
echo DCR_CONNECTION_PORT : %DCR_CONNECTION_PORT%
echo DCR_CONTAINER_PORT  : %DCR_CONTAINER_PORT%
echo VERSION             : %DCR_VERSION%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

echo Docker stop/rm dcr_db ...................................... before:
docker ps -a
docker ps    | find "dcr_db" && docker stop dcr_db
docker ps -a | find "dcr_db" && docker rm --force dcr_db
echo ............................................................. after:
docker ps -a

resources\Gammadyne\timer.exe

rem ------------------------------------------------------------------------------
rem PostgreSQL                          https://hub.docker.com/_/postgres
rem ------------------------------------------------------------------------------

echo PostgreSQL
echo --------------------------------------------------------------------------------
echo Docker create dcr_db (PostgreSQL %DCR_VERSION%)

docker create -e        POSTGRES_DB=dcr_db_admin ^
              -e        POSTGRES_HOST_AUTH_METHOD=password ^
              -e        POSTGRES_PASSWORD=postgresql ^
              -e        POSTGRES_USER=dcr_user_admin ^
              --name    dcr_db ^
              -p        %DCR_CONNECTION_PORT%:%DCR_CONTAINER_PORT% ^
              postgres:%DCR_VERSION%

echo Docker start  dcr_db (PostgreSQL %DCR_VERSION%) ...
docker start dcr_db

ping -n 30 127.0.0.1>nul

for /f "delims=" %%A in ('resources\Gammadyne\timer.exe /s') do set "CONSUMED=%%A"
echo DOCKER PostgreSQL was ready in %CONSUMED%

docker ps

echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
