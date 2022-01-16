@echo off

rem --------------------------------------------------------------------------------
rem
rem run_dcr.bat: Document Content Recognition.
rem
rem --------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTIONS_DEFAULT=pdf

if exist dcr.log del /f /q dcr.log

if ["%1"] EQU [""] (
    echo ===============================================================================
    echo pdf                  - Convert the files in the inbox to pdf format.
    echo -------------------------------------------------------------------------------
    set /P DCR_CHOICE_ACTIONS="Enter the desired action [default: %DCR_CHOICE_ACTIONS_DEFAULT%] "

    if ["!DCR_CHOICE_ACTIONS!"] EQU [""] (
        set DCR_CHOICE_ACTIONS=%DCR_CHOICE_ACTIONS_DEFAULT%
    )
) else (
    set DCR_CHOICE_ACTIONS=%1
)

set ERRORLEVEL=0

echo.
echo Script %0 is now running
echo.
echo You can find the run log in the file run_dcr.log
echo.
echo Please wait ...
echo.

rem > run_dcr.log 2>&1 (

    echo ===============================================================================
    echo Start %0
    echo -------------------------------------------------------------------------------
    echo dcr - Document Content Recognition.
    echo -------------------------------------------------------------------------------
    echo CHOICE_ACTIONS                 : %DCR_CHOICE_ACTIONS%
    echo -------------------------------------------------------------------------------
    echo:| TIME
    echo ===============================================================================
   
    make
    if %ERRORLEVEL% neq 0 (
        echo Processing of the script: %0 - step: 'make' was aborted, error code=%ERRORLEVEL%
        exit -1073741510
    )
    
    python dcr/dcr.py %DCR_CHOICE_ACTIONS%
    if %ERRORLEVEL% neq 0 (
        echo Processing of the script: %0 - step: 'python dcr/dcr.py' was aborted, error code=%ERRORLEVEL%
        exit -1073741510
    )    

    echo -------------------------------------------------------------------------------
    echo:| TIME
    echo -------------------------------------------------------------------------------
    echo End   %0
    echo ===============================================================================
rem )
