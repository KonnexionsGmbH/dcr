@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr_dev.bat: Document Content Recognition - Development Environment.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CHOICE_ACTION_DEFAULT=aui
set DCR_ENVIRONMENT_TYPE=dev
set PYTHONPATH=%PYTHONPATH%;src

if ["%1"] EQU [""] (
    echo =========================================================
    echo aui          - Run the administration user interface.
    echo ---------------------------------------------------------
    echo all          - Run the complete core processing of all new documents.
    echo ---------------------------------------------------------
    echo p_i          - 1. Process the inbox directory.
    echo p_2_i[_only] - 2. Convert pdf documents to image files:          pdf2image / Poppler.
    echo ocr[_only]   - 3. Convert image files to pdf documents:          Tesseract OCR / Tex Live.
    echo n_2_p[_only] - 2. Convert non-pdf documents to pdf documents:    Pandoc
    echo ---------------------------------------------------------
    echo tet[_only]   - 4. Extract text and metadata from pdf documents:  PDFlib TET.
    echo s_p_j[_only] - 5. Store the parser result in a JSON file.
    echo tkn[_only]   - 6. Create qualified document tokens.              SpaCy.
    echo ---------------------------------------------------------
    echo db_c         - Create the database.
    echo db_u         - Upgrade the database.
    echo ---------------------------------------------------------
    echo e_lt         - Export the line type rules.
    echo ---------------------------------------------------------
    echo m_d          - Run the installation of the necessary 3rd party packages for development and run the development ecosystem.
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
    )

    goto normal_exit
)

if ["%DCR_CHOICE_ACTION%"] EQU ["all"] (
    if exist data\inbox_%DCR_ENVIRONMENT_TYPE% (
        rd /s /q data\inbox_%DCR_ENVIRONMENT_TYPE%
    )
    if exist data\inbox_%DCR_ENVIRONMENT_TYPE%_accepted (
        rd /s /q data\inbox_%DCR_ENVIRONMENT_TYPE%_accepted
    )
    if exist data\inbox_%DCR_ENVIRONMENT_TYPE%_rejected (
        rd /s /q data\inbox_%DCR_ENVIRONMENT_TYPE%_rejected
    )
    mkdir data\inbox_%DCR_ENVIRONMENT_TYPE%
    xcopy /E /I /Q tests\inbox data\inbox_%DCR_ENVIRONMENT_TYPE%
    dir data\inbox_%DCR_ENVIRONMENT_TYPE%
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["aui"] (
    pipenv run python src\dcr\admin.py
    if ERRORLEVEL 1 (
        echo Processing of the script: %0 - step: 'python src\dcr\admin.py was aborted
    )
    goto normal_exit
)

if ["%DCR_CHOICE_ACTION%"] EQU ["db_c"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["db_u"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["e_lt"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["n_2_p"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["n_2_p_only"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["ocr"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["ocr_only"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["p_i"] (
    if exist data\inbox_%DCR_ENVIRONMENT_TYPE% (
        rd /s /q data\inbox_%DCR_ENVIRONMENT_TYPE%
    )
    if exist data\inbox_%DCR_ENVIRONMENT_TYPE%_accepted (
        rd /s /q data\inbox_%DCR_ENVIRONMENT_TYPE%_accepted
    )
    if exist data\inbox_%DCR_ENVIRONMENT_TYPE%_rejected (
        rd /s /q data\inbox_%DCR_ENVIRONMENT_TYPE%_rejected
    )
    mkdir data\inbox_%DCR_ENVIRONMENT_TYPE%
    xcopy /E /I /Q tests\inbox data\inbox_%DCR_ENVIRONMENT_TYPE%
    dir data\inbox_%DCR_ENVIRONMENT_TYPE%
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i_only"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["s_p_j"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["s_p_j_only"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["tet"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["tet_only"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["%DCR_CHOICE_ACTION%"] EQU ["tkn"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)
if ["%DCR_CHOICE_ACTION%"] EQU ["tkn_only"] (
    set _CHOICE=%DCR_CHOICE_ACTION%
)

if ["!_CHOICE!"] EQU ["%DCR_CHOICE_ACTION%"] (
    if ["%DCR_CHOICE_ACTION%"] EQU ["e_lt"] (
        set DCR_CHOICE_ACTION=e_lt
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i"] (
        set DCR_CHOICE_ACTION=p_i %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["p_2_i_only"] (
        set DCR_CHOICE_ACTION=p_2_i
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["ocr"] (
        set DCR_CHOICE_ACTION=p_i p_2_i %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["ocr_only"] (
        set DCR_CHOICE_ACTION=ocr
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["n_2_p"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["n_2_p_only"] (
        set DCR_CHOICE_ACTION=n_2_p
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["tet"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["tet_only"] (
        set DCR_CHOICE_ACTION=tet
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["s_p_j"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["s_p_j_only"] (
        set DCR_CHOICE_ACTION=s_p_j
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["tkn"] (
        set DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet s_p_j tkn %DCR_CHOICE_ACTION%
    )
    if ["%DCR_CHOICE_ACTION%"] EQU ["tkn_only"] (
        set DCR_CHOICE_ACTION=tkn
    )

    pipenv run python src\dcr\dcr.py !DCR_CHOICE_ACTION!
    if ERRORLEVEL 1 (
        echo Processing of the script: %0 - step: 'python src\dcr\dcr.py %DCR_CHOICE_ACTION%' was aborted
    )

    goto normal_exit
)

echo Usage: "run_dcr_dev[.bat] all | db_c | db_u | e_lt | m_d | n_2_p[_only] | ocr[_only] | p_i | p_2_i[_only] | s_p_j[_only] | tet[_only] | tkn[_only]"

:normal_exit
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
