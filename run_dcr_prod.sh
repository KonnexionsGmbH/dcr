#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr_prod.sh: Document Content Recognition - Production Environment.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=db_u
export DCR_ENVIRONMENT_TYPE=prod
export PYTHONPATH=${PYTHONPATH}:src/dcr

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "aui   - Run the administration user interface."
    echo "------------------------------------------------------------------------------"
    echo "all   - Run the complete processing of all new documents."
    echo "------------------------------------------------------------------------------"
    echo "p_i   - 1. Process the inbox directory."
    echo "p_2_i - 2. Convert pdf documents to image files:               Poppler."
    echo "ocr   - 3. Convert image documents to pdf files:               Tesseract OCR."
    echo "n_2_p - 2. Convert non-pdf documents to pdf files:             Pandoc."
    echo "tet   - 4. Extract text and metadata from pdf documents:       PDFlib TET."
    echo "s_f_p - 5. Store the document structure from the parser result."
    echo "------------------------------------------------------------------------------"
    echo "db_c  - Create the database."
    echo "db_u  - Upgrade the database."
    echo "------------------------------------------------------------------------------"
    echo "m_d   - Run the installation of the necessary 3rd party packages for development and run the development ecosystem."
    echo "m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules."
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired action [default: ${DCR_CHOICE_ACTION_DEFAULT}] " DCR_CHOICE_ACTION
    export DCR_CHOICE_ACTION=${DCR_CHOICE_ACTION:-$DCR_CHOICE_ACTION_DEFAULT}
else
    export DCR_CHOICE_ACTION=$1
fi

echo ""
echo "Script $0 is now running"

rm -f run_dcr_prod_debug.log
export LOG_FILE=run_dcr_prod_${DCR_CHOICE_ACTION}.log
rm -f run_dcr_prod_${DCR_CHOICE_ACTION}.log

echo ""
echo "You can find the run log in the file ${LOG_FILE}"
echo ""

exec &> >(tee -i ${LOG_FILE}) 2>&1
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
    if ! ( pipenv run python src/dcr/admin.py ); then
        exit 255
    fi
    ;;
  m_d)
    # Development install packages
    if ! ( make pipenv-dev ); then
        exit 255
    fi
    ;;
  m_p)
    # Production install packages
    if ! ( make pipenv-prod ); then
        exit 255
    fi
    # Production compile all
    if ! ( make compileall ); then
        exit 255
    fi
    ;;
  all|db_c|db_u|n_2_p|ocr|p_i|p_2_i|s_f_p|tet)
    case "${DCR_CHOICE_ACTION}" in
      p_2_i)
        export DCR_CHOICE_ACTION=p_i ${DCR_CHOICE_ACTION}
        ;;
      ocr)
        export DCR_CHOICE_ACTION=p_i p_2_i ${DCR_CHOICE_ACTION}
        ;;
      n_2_p)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr ${DCR_CHOICE_ACTION}
        ;;
      tet)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p ${DCR_CHOICE_ACTION}
        ;;
      s_f_p)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet ${DCR_CHOICE_ACTION}
        ;;
      *)
        ;;
    esac
    if ! ( pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}" ); then
        exit 255
    fi
    ;;
  *)
    echo "Usage: ./run_dcr_prod.sh all | db_c | db_u | m_d | m_p | n_i_p | ocr | p_i | p_2_i | s_f_p | tet"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
