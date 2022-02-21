@echo off

rem ------------------------------------------------------------------------------
rem
rem run_setup_postgresql.bat: Setup a PostgreSQL Docker container.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_ENVIRONMENT_TYPE_DEFAULT=dev

if ["%DCR_CONTAINER_PORT%"] EQU [""] (
    set DCR_CONTAINER_PORT=5432
)

if ["%DCR_VERSION%"] EQU [""] (
    set DCR_VERSION=latest
)

if ["%1"] EQU [""] (
    echo =========================================================
    echo dev  - Environment Development.
    echo prod - Environment Production.
    echo test - Environment Test.
    echo ---------------------------------------------------------
    set /P DCR_ENVIRONMENT_TYPE="Enter the desired environment [default: %DCR_ENVIRONMENT_TYPE_DEFAULT%] "

    if ["!DCR_ENVIRONMENT_TYPE!"] EQU [""] (
        set DCR_ENVIRONMENT_TYPE=%DCR_ENVIRONMENT_TYPE_DEFAULT%
    )
) else (
    set DCR_ENVIRONMENT_TYPE=%1
)

if ["%DCR_CONNECTION_PORT%"] EQU [""] (
    if ["%DCR_ENVIRONMENT_TYPE%"] EQU ["dev"] (
        set DCR_CONNECTION_PORT=5432
    )
    if ["%DCR_ENVIRONMENT_TYPE%"] EQU ["prod"] (
        set DCR_CONNECTION_PORT=5433
    )
    if ["%DCR_ENVIRONMENT_TYPE%"] EQU ["test"] (
        set DCR_CONNECTION_PORT=5434
    )
)

echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo DCR - Setup a PostgreSQL Docker container.
echo --------------------------------------------------------------------------------
echo CONNECTION_PORT    : %DCR_CONNECTION_PORT%
echo CONTAINER_PORT     : %DCR_CONTAINER_PORT%
echo ENVIRONMENT        : %DCR_ENVIRONMENT_TYPE%
echo POSTGRESQL VERSION : %DCR_VERSION%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

echo Docker stop/rm dcr_db_%DCR_ENVIRONMENT_TYPE% .................... before:
docker ps -a
docker ps    | find "dcr_db_%DCR_ENVIRONMENT_TYPE%" && docker stop dcr_db_%DCR_ENVIRONMENT_TYPE%
docker ps -a | find "dcr_db_%DCR_ENVIRONMENT_TYPE%" && docker rm --force dcr_db_%DCR_ENVIRONMENT_TYPE%
echo ............................................................. after:
docker ps -a

resources\Gammadyne\timer.exe

rem ------------------------------------------------------------------------------
rem PostgreSQL                          https://hub.docker.com/_/postgres
rem ------------------------------------------------------------------------------

echo PostgreSQL
echo --------------------------------------------------------------------------------
echo Docker create dcr_db_%DCR_ENVIRONMENT_TYPE% (PostgreSQL %DCR_VERSION%)

docker create -e        POSTGRES_DB=dcr_db_%DCR_ENVIRONMENT_TYPE%_admin ^
              -e        POSTGRES_HOST_AUTH_METHOD=password ^
              -e        POSTGRES_PASSWORD=postgresql ^
              -e        POSTGRES_USER=dcr_user_admin ^
              --name    dcr_db_%DCR_ENVIRONMENT_TYPE% ^
              -p        %DCR_CONNECTION_PORT%:%DCR_CONTAINER_PORT% ^
              postgres:%DCR_VERSION%

echo Docker start  dcr_db_%DCR_ENVIRONMENT_TYPE% (PostgreSQL %DCR_VERSION%) ...
docker start dcr_db_%DCR_ENVIRONMENT_TYPE%

ping -n 30 127.0.0.1>nul

for /f "delims=" %%A in ('resources\Gammadyne\timer.exe /s') do set "CONSUMED=%%A"
echo DOCKER PostgreSQL was ready in %CONSUMED%

docker ps

echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
