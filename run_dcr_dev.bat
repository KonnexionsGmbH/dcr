@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr_dev.bat: Document Content Recognition - Development Environment.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTION_DEFAULT=db_u
set DCR_ENVIRONMENT_TYPE=dev
set PYTHONPATH=src/dcr

if ["%1"] EQU [""] (
    echo =========================================================
    echo all   - Run the complete processing of all new documents.
    echo db_c  - Create the database.
    echo db_u  - Upgrade the database.
    echo m_d   - Run the installation of the necessary 3rd party packages for development and run the development ecosystem.
    echo m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules.
    echo p_i   - Process the inbox directory.
    echo p_2_i - Convert pdf documents to image files.
    echo ---------------------------------------------------------
    set /P DCR_CHOICE_ACTION="Enter the desired action [default: %DCR_CHOICE_ACTION_DEFAULT%] "

    if ["!DCR_CHOICE_ACTION!"] EQU [""] (
        set DCR_CHOICE_ACTION=%DCR_CHOICE_ACTION_DEFAULT%
    )
) else (
    set DCR_CHOICE_ACTION=%1
)

echo.
echo Script %0 is now running

if exist run_dcr_dev_debug.log del /f /q run_dcr_dev_debug.log
set LOG_FILE=run_dcr_dev.log
if exist run_dcr_dev.log      del /f /q run_dcr_dev.log

echo.
echo You can find the run log in the file %LOG_FILE%
echo.
echo Please wait ...
echo.

REM > %LOG_FILE% 2>&1 (

    echo =======================================================================
    echo Start %0
    echo -----------------------------------------------------------------------
    echo DCR - Document Content Recognition.
    echo -----------------------------------------------------------------------
    echo CHOICE_ACTION    : %DCR_CHOICE_ACTION%
    echo ENVIRONMENT_TYPE : %DCR_ENVIRONMENT_TYPE%
    echo PYTHONPATH       : %PYTHONPATH%
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo =======================================================================

    set _CHOICE=

    if ["%DCR_CHOICE_ACTION%"] EQU ["m_d"] (
        make pipenv-dev
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make inst_dev' was aborted
        )
        make dev
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make eco_dev' was aborted
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["m_p"] (
        make pipenv-prod
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make prod' was aborted
        )
        make compileall
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make prod' was aborted
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["all"]   set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["db_c"]  (
        if exist data\dcr.db del /f /q data\dcr.db
        set _CHOICE=%DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["db_u"]  (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["all"]   (
        if exist data\inbox rmdir /s /q data\inbox
        mkdir data\inbox
        xcopy /E /I tests\inbox data\inbox
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["p_i"]   (
        if exist data\inbox rmdir /s /q data\inbox
        mkdir data\inbox
        xcopy /E /I tests\inbox data\inbox
        set _CHOICE=%DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"]   (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%_CHOICE%"] EQU ["%DCR_CHOICE_ACTION%"] (
        pipenv run python src\dcr\dcr.py %DCR_CHOICE_ACTION%
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'python src\dcr\dcr.py %DCR_CHOICE_ACTION%' was aborted
        )
        goto normal_exit
    )

    echo Usage: "run_dcr_dev[.bat] all | db_c | db_u | m_d | m_p | p_i | p_2_i"

    :normal_exit
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo -----------------------------------------------------------------------
    echo End   %0
    echo =======================================================================
REM )