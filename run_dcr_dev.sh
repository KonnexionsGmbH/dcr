#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr_dev.sh: Document Content Recognition - Development Environment.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=aui
export DCR_ENVIRONMENT_TYPE=dev
export PYTHONPATH=${PYTHONPATH}:src/dcr

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "aui          - Run the administration user interface."
    echo "------------------------------------------------------------------------------"
    echo "all          - Run the complete processing of all new documents."
    echo "------------------------------------------------------------------------------"
    echo "p_i          - 1. Process the inbox directory."
    echo "p_2_i[_only] - 2. Convert pdf documents to image files:         pdf2image / Poppler."
    echo "ocr[_only]   - 3. Convert image documents to pdf files:         Tesseract OCR / Tex Live."
    echo "n_2_p[_only] - 2. Convert non-pdf documents to pdf files:       Pandoc."
    echo "------------------------------------------------------------------------------"
    echo "tet[_only]   - 4. Extract text and metadata from pdf documents: PDFlib TET."
    echo "s_f_p[_only] - 5. Store the parser result in the database."
    echo "tkn[_only]   - 6. Create qualified document tokens.             SpaCy."
    echo "------------------------------------------------------------------------------"
    echo "db_c         - Create the database."
    echo "db_u         - Upgrade the database."
    echo "------------------------------------------------------------------------------"
    echo "m_d          - Run the installation of the necessary 3rd party packages for development and run the development ecosystem."
    echo "m_p          - Run the installation of the necessary 3rd party packages for production and compile all packages and modules."
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired action [default: ${DCR_CHOICE_ACTION_DEFAULT}] " DCR_CHOICE_ACTION
    export DCR_CHOICE_ACTION=${DCR_CHOICE_ACTION:-$DCR_CHOICE_ACTION_DEFAULT}
else
    export DCR_CHOICE_ACTION=$1
fi

echo ""
echo "Script $0 is now running"

rm -f run_dcr_debug.log
export LOG_FILE=run_dcr_dev.log
rm -f run_dcr_dev.log

echo ""
echo "You can find the run log in the file $LOG_FILE"
echo ""

exec &> >(tee -i $LOG_FILE) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "DCR - Document Content Recognition."
echo "------------------------------------------------------------------------------"
echo "CHOICE_ACTION    : ${DCR_CHOICE_ACTION}"
echo "ENVIRONMENT_TYPE : ${DCR_ENVIRONMENT_TYPE}"
echo "PYTHONPATH       : ${PYTHONPATH}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="

case "${DCR_CHOICE_ACTION}" in
  aui)
    pipenv run python src/dcr/admin.py
    ;;
  m_d)
    # Development install packages
    make pipenv-dev
    ;;
  m_p)
    # Production install packages
    make pipenv-prod
    # Production compile all
    make compileall
    ;;
  db_c)
    pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}"
    ;;
  db_u|n_2_p|ocr|p_2_i|s_f_p|tet|tkn)
    case "${DCR_CHOICE_ACTION}" in
      n_2_p)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr ${DCR_CHOICE_ACTION}
        ;;
      n_2_p_only)
        export DCR_CHOICE_ACTION=n_2_p
        ;;
      ocr)
        export DCR_CHOICE_ACTION=p_i p_2_i ${DCR_CHOICE_ACTION}
        ;;
      ocr_only)
        export DCR_CHOICE_ACTION=ocr
        ;;
      p_2_i)
        export DCR_CHOICE_ACTION=p_i ${DCR_CHOICE_ACTION}
        ;;
      p_2_i_only)
        export DCR_CHOICE_ACTION=p_2_i
        ;;
      s_f_p)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet ${DCR_CHOICE_ACTION}
        ;;
      s_f_p_only)
        export DCR_CHOICE_ACTION=s_f_p
        ;;
      tet)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p ${DCR_CHOICE_ACTION}
        ;;
      tet_only)
        export DCR_CHOICE_ACTION=tet
        ;;
      tkn)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet s_f_p ${DCR_CHOICE_ACTION}
        ;;
      tkn_only)
        export DCR_CHOICE_ACTION=tkn
        ;;
      *)
        ;;
    esac
    pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}"
    ;;
  all|p_i)
    rm -rf data/inbox_${DCR_ENVIRONMENT_TYPE}
    mkdir data/inbox_${DCR_ENVIRONMENT_TYPE}
    cp -r tests/inbox/* data/inbox_${DCR_ENVIRONMENT_TYPE}
    ls -ll data/inbox_${DCR_ENVIRONMENT_TYPE}
    pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}"
    ;;
  *)
    echo "Usage: ./run_dcr_dev.sh all | db_c | db_u | m_d | m_p | n_i_p[_only] | ocr[_only] | p_i | p_2_i[_only] | s_f_p[_only] | tet[_only] | tkn[_only]"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
