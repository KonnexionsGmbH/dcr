@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr_prod.bat: Document Content Recognition - Production Environment.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTION_DEFAULT=db_u
set DCR_ENVIRONMENT_TYPE=prod
set PYTHONPATH=src/dcr

if ["%1"] EQU [""] (
    echo =========================================================
    echo all   - Run the complete processing of all new documents.
    echo db_c  - Create the database.
    echo db_u  - Upgrade the database.
    echo m_d   - Run the installation of the necessary 3rd party packages for development and run the development ecosystem.
    echo m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules.
    echo n_2_p - Convert non-pdf documents to pdf files.
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

if exist run_dcr_prod_debug.log (
    del /f /q run_dcr_prod_debug.log
)
set LOG_FILE=run_dcr_prod.log
if exist run_dcr_prod.log (
    del /f /q run_dcr_prod.log
)

echo.
echo You can find the run log in the file %LOG_FILE%
echo.
echo Please wait ...
echo.

%LOG_FILE% 2>&1 (

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
            exit -1073741510
        )
        make dev
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make eco_dev' was aborted
            exit -1073741510
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["m_p"] (
        make pipenv-prod
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make prod' was aborted
            exit -1073741510
        )
        make compileall
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'make prod' was aborted
            exit -1073741510
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["all"] (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["db_c"] (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["db_u"] (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["n_2_p"] (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["p_i"] (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"] (
        set _CHOICE=%DCR_CHOICE_ACTION%
    )

    if ["%_CHOICE%"] EQU ["%DCR_CHOICE_ACTION%"] (
        pipenv run python src\dcr\dcr.py %DCR_CHOICE_ACTION%
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'python src\dcr\dcr.py %DCR_CHOICE_ACTION%' was aborted
            exit -1073741510
        )
        goto normal_exit
    )

    echo Usage: "run_dcr_prod[.bat] all | db_c | db_u | m_d | m_p | n_2_p | p_i | p_2_i"
    exit -1073741510

    :normal_exit
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo -----------------------------------------------------------------------
    echo End   %0
    echo =======================================================================
REM )
