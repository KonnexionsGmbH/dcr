#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr_dev.sh: Document Content Recognition - Development Environment.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=db_u
export DCR_ENVIRONMENT_TYPE=dev
export PYTHONPATH=src

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "all          - Run the complete processing of all new documents."
    echo "------------------------------------------------------------------------------"
    echo "p_i          - 1. Process the inbox directory."
    echo "p_2_i[_only] - 2. Convert pdf documents to image files:         pdf2image / Poppler."
    echo "ocr[_only]   - 3. Convert image files to pdf documents:         Tesseract OCR / Tex Live."
    echo "n_2_p[_only] - 2. Convert non-pdf documents to pdf documents:   Pandoc."
    echo "------------------------------------------------------------------------------"
    echo "tet[_only]   - 4. Extract text and metadata from pdf documents: PDFlib TET."
    echo "s_p_j[_only] - 5. Store the parser result in a JSON file."
    echo "tkn[_only]   - 6. Create qualified document tokens.             SpaCy."
    echo "------------------------------------------------------------------------------"
    echo "db_c         - Create the database."
    echo "db_u         - Upgrade the database."
    echo "------------------------------------------------------------------------------"
    echo "e_lt         - Export the line type rules."
    echo "------------------------------------------------------------------------------"
    echo "m_d          - Run the installation of the necessary 3rd party packages for development and run the development ecosystem."
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired action [default: ${DCR_CHOICE_ACTION_DEFAULT}] " DCR_CHOICE_ACTION
    export DCR_CHOICE_ACTION=${DCR_CHOICE_ACTION:-$DCR_CHOICE_ACTION_DEFAULT}
else
    export DCR_CHOICE_ACTION=$1
fi

echo ""
echo "Script $0 is now running"

rm -f logging_dcr.log
export LOG_FILE=run_dcr_dev_${DCR_CHOICE_ACTION}.log
rm -f run_dcr_dev_${DCR_CHOICE_ACTION}.log

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
  m_d)
    # Development install packages
    make pipenv-dev
    ;;
  db_c)
    pipenv run python src/dcr/launcher.py "${DCR_CHOICE_ACTION}"
    ;;
  db_u|e_lt|n_2_p|ocr|p_2_i|s_p_j|tet|tkn)
    case "${DCR_CHOICE_ACTION}" in
      e_lt)
        export DCR_CHOICE_ACTION=e_lt
        ;;
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
      s_p_j)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet ${DCR_CHOICE_ACTION}
        ;;
      s_p_j_only)
        export DCR_CHOICE_ACTION=s_p_j
        ;;
      tet)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p ${DCR_CHOICE_ACTION}
        ;;
      tet_only)
        export DCR_CHOICE_ACTION=tet
        ;;
      tkn)
        export DCR_CHOICE_ACTION=p_i p_2_i ocr n_2_p tet s_p_j ${DCR_CHOICE_ACTION}
        ;;
      tkn_only)
        export DCR_CHOICE_ACTION=tkn
        ;;
      *)
        ;;
    esac
    pipenv run python src/dcr/launcher.py "${DCR_CHOICE_ACTION}"
    ;;
  all|p_i)
    rm -rf data/inbox_${DCR_ENVIRONMENT_TYPE}
    mkdir data/inbox_${DCR_ENVIRONMENT_TYPE}
    cp -r tests/inbox/* data/inbox_${DCR_ENVIRONMENT_TYPE}
    ls -ll data/inbox_${DCR_ENVIRONMENT_TYPE}
    pipenv run python src/dcr/launcher.py "${DCR_CHOICE_ACTION}"
    ;;
  *)
    echo "Usage: ./run_dcr_dev.sh all | db_c | db_u | e_lt | m_d | n_i_p[_only] | ocr[_only] | p_i | p_2_i[_only] | s_p_j[_only] | tet[_only] | tkn[_only]"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
