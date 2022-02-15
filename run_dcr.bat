@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr.bat: Document Content Recognition.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTION_DEFAULT=db_c

if ["%1"] EQU [""] (
    echo =========================================================
    echo all   - Run the complete processing of all new documents.
    echo db_c  - Create the database.
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

set LOG_FILE=run_dcr.log
if exist run_dcr.log       del /f /q run_dcr.log
if exist run_dcr_debug.log del /f /q run_dcr_debug.log

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
    echo CHOICE_ACTION : %DCR_CHOICE_ACTION%
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

    if ["%DCR_CHOICE_ACTION%"] EQU ["all"]   set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["db_c"]  set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["p_i"]   set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"]   set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%_CHOICE%"] EQU ["%DCR_CHOICE_ACTION%"] (
        pipenv run python src\dcr\dcr.py %DCR_CHOICE_ACTION%
        if ERRORLEVEL 1 (
            echo Processing of the script: %0 - step: 'python src\dcr\dcr.py %DCR_CHOICE_ACTION%' was aborted
            exit -1073741510
        )
        goto normal_exit
    )

    echo Usage: "run_dcr[.bat] all | db_c | m_d | m_p | p_i | p_2_i"
    exit -1073741510

    :normal_exit
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo -----------------------------------------------------------------------
    echo End   %0
    echo =======================================================================
REM )
