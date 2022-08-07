#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr_prod.sh: Document Content Recognition - Production Environment.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=db_u
export DCR_ENVIRONMENT_TYPE=prod
export PYTHONPATH=src

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "all   - Run the complete processing of all new documents."
    echo "------------------------------------------------------------------------------"
    echo "p_i   - 1. Process the inbox directory."
    echo "p_2_i - 2. Convert pdf documents to image files:         pdf2image / Poppler."
    echo "ocr   - 3. Convert image files to pdf documents:         Tesseract OCR / Tex Live."
    echo "n_2_p - 2. Convert non-pdf documents to pdf documents:   Pandoc."
    echo "------------------------------------------------------------------------------"
    echo "tet   - 4. Extract text and metadata from pdf documents: PDFlib TET."
    echo "s_p_j - 5. Store the parser result in a JSON file."
    echo "tkn   - 6. Create qualified document tokens.             SpaCy."
    echo "------------------------------------------------------------------------------"
    echo "db_c  - Create the database."
    echo "db_u  - Upgrade the database."
    echo "------------------------------------------------------------------------------"
    echo "e_lt  - Export the line type rules."
    echo "------------------------------------------------------------------------------"
    echo "m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules."
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired action [default: ${DCR_CHOICE_ACTION_DEFAULT}] " DCR_CHOICE_ACTION
    export DCR_CHOICE_ACTION=${DCR_CHOICE_ACTION:-$DCR_CHOICE_ACTION_DEFAULT}
else
    export DCR_CHOICE_ACTION=$1
fi

echo ""
echo "Script $0 is now running"

rm -f run_dcr_debug.log
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
  all|db_c|db_u|e_lt|n_2_p|ocr|p_i|p_2_i|s_p_j|tet|tkn)
    case "${DCR_CHOICE_ACTION}" in
      e_lt)
        export DCR_CHOICE_ACTION=e_lt
        ;;
      p_2_i)
        export DCR_CHOICE_ACTION=p_i ${DCR_CHOICE_ACTION?}
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
      s_p_j)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet ${DCR_CHOICE_ACTION}
        ;;
      tkn|all)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet s_p_j ${DCR_CHOICE_ACTION}
        ;;
      *)
        ;;
    esac
    if ! ( pipenv run python src/dcr/launcher.py "${DCR_CHOICE_ACTION}" ); then
        exit 255
    fi
    ;;
  *)
    echo "Usage: ./run_dcr_prod.sh all | db_c | db_u | e_lt | m_p | n_i_p | ocr | p_i | p_2_i | s_p_j | tet | tkn"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
