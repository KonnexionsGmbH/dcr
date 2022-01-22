@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr.bat: Document Content Recognition.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTION_DEFAULT=d_c_u

if ["%1"] EQU [""] (
    echo =========================================================
    echo d_c_u           - Create or upgrade the database
    echo m_d_e           - Run the development ecosystem
    echo m_d_i           - Run the installation of the necessary 3rd party packages for development
    echo m_p             - Run the installation of the necessary 3rd party packages for production and compile all packages and modules
    echo new             - Run the complete processing of all new documents
    echo p_i             - Process input folder
    echo p_i_o           - Process input folder OCR
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

echo.
echo You can find the run log in the file %LOG_FILE%
echo.
echo Please wait ...
echo.

REM > %LOG_FILE% 2>&1 (

    echo =======================================================================
    echo Start %0
    echo -----------------------------------------------------------------------
    echo dcr - Document Content Recognition.
    echo -----------------------------------------------------------------------
    echo CHOICE_ACTION : %DCR_CHOICE_ACTION%
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo =======================================================================

    set _CHOICE=

    if ["%DCR_CHOICE_ACTION%"] EQU ["d_c_u"] set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["m_d_e"] (
        make eco_dev
        if %ERRORLEVEL% neq 0 (
            echo Processing of the script: %0 - step: 'make eco_dev' was aborted, error code=%ERRORLEVEL%
            exit -1073741510
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["m_d_i"] (
        make inst_dev
        if %ERRORLEVEL% neq 0 (
            echo Processing of the script: %0 - step: 'make inst_dev' was aborted, error code=%ERRORLEVEL%
            exit -1073741510
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["m_p"] (
        make prod
        if %ERRORLEVEL% neq 0 (
            echo Processing of the script: %0 - step: 'make prod' was aborted, error code=%ERRORLEVEL%
            exit -1073741510
        )
        goto normal_exit
    )

    if ["%DCR_CHOICE_ACTION%"] EQU ["new"]   set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["p_i"]   set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%DCR_CHOICE_ACTION%"] EQU ["p_i_o"] set _CHOICE=%DCR_CHOICE_ACTION%

    if ["%_CHOICE%"] EQU ["%DCR_CHOICE_ACTION%"] (
        python src\dcr\app.py %DCR_CHOICE_ACTION%
        if %ERRORLEVEL% neq 0 (
            echo Processing of the script: %0 - step: 'python src\dcr\app.py %DCR_CHOICE_ACTION%' was aborted, error code=%ERRORLEVEL%
            exit -1073741510
        )
        goto normal_exit
    )

    echo Usage: "./run_dcr.sh d_c_u | m_d_e | m_d_i | m_p | new | p_i | p_i_o"
    exit -1073741510

    :normal_exit
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo -----------------------------------------------------------------------
    echo End   %0
    echo =======================================================================
REM )
