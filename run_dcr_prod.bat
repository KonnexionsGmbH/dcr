@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr_prod.bat: Document Content Recognition - Production Environment.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTION_DEFAULT=aui
set DCR_ENVIRONMENT_TYPE=prod
set PYTHONPATH=%PYTHONPATH%;src\dcr

if ["%1"] EQU [""] (
    echo =========================================================
    echo aui   - Run the administration user interface.
    echo ---------------------------------------------------------
    echo all   - Run the complete core processing of all new documents.
    echo ---------------------------------------------------------
    echo p_i   - 1. Process the inbox directory.
    echo p_2_i - 2. Convert pdf documents to image files:          pdf2image / Poppler.
    echo ocr   - 3. Convert image files to pdf documents:          Tesseract OCR / Tex Live.
    echo n_2_p - 2. Convert non-pdf documents to pdf documents:    Pandoc
    echo ---------------------------------------------------------
    echo tet   - 4. Extract text and metdata from pdf documents:   PDFlib TET.
    echo s_p_j - 5. Store the parser result in a JSON file.
    echo tkn   - 6. Create qualified document tokens.              SpaCy.
    echo ---------------------------------------------------------
    echo db_c  - Create the database.
    echo db_u  - Upgrade the database.
    echo ---------------------------------------------------------
    echo m_d   - Run the installation of the necessary 3rd party packages for development and run the development ecosystem.
    echo m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules.
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

if exist run_dcr_debug.log (
    del /f /q run_dcr_debug.log
)

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

if ["%DCR_CHOICE_ACTION%"] EQU ["aui"] (
    pipenv run python src\dcr\admin.py
    if ERRORLEVEL 1 (
        echo Processing of the script: %0 - step: 'python src\dcr\admin.py' was aborted
        exit -1073741510
    )
    goto normal_exit
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

if ["%DCR_CHOICE_ACTION%"] EQU ["ocr"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["p_i"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["s_p_j"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["tet"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["tkn"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["!_CHOICE!"] EQU ["%DCR_CHOICE_ACTION%"] (
    if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"] (
        set DCR_CHOICE_ACTION=p_i %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["ocr"] (
        set DCR_CHOICE_ACTION=p_i p_2_i %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["n_2_p"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["tet"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["s_p_j"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["tkn"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet s_p_j tkn %DCR_CHOICE_ACTION%
    )
    pipenv run python src\dcr\dcr.py !DCR_CHOICE_ACTION!
    if ERRORLEVEL 1 (
        echo Processing of the script: %0 - step: 'python src\dcr\dcr.py %DCR_CHOICE_ACTION%' was aborted
        exit -1073741510
    )
    goto normal_exit
)

echo Usage: "run_dcr_prod[.bat] all | db_c | db_u | m_d | m_p | n_2_p | ocr | p_i | p_2_i | s_p_j | tet | tkn"
exit -1073741510

:normal_exit
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
