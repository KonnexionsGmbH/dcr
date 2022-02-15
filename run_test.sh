#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_test.sh: Document Content Recognition.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=db_c
export PYTHONPATH=src/dcr

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "all   - Run the complete processing of all new documents."
    echo "db_c  - Create the database."
    echo "m_d   - Run the installation of the necessary 3rd party packages for development and run the development ecosystem."
    echo "m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules."
    echo "p_i   - Process the inbox directory."
    echo "p_2_i - Convert pdf documents to image files."
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired action [default: ${DCR_CHOICE_ACTION_DEFAULT}] " DCR_CHOICE_ACTION
    export DCR_CHOICE_ACTION=${DCR_CHOICE_ACTION:-$DCR_CHOICE_ACTION_DEFAULT}
else
    export DCR_CHOICE_ACTION=$1
fi

echo ""
echo "Script $0 is now running"

export LOG_FILE=run_test.log
rm -f run_test.log
rm -f run_dcr_debug.log

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
echo "CHOICE_ACTION : ${DCR_CHOICE_ACTION}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="

case "${DCR_CHOICE_ACTION}" in
  m_d)
    # Development install packages
    make pipenv-dev
    # Development ecosystem
    make dev
    ;;
  m_p)
    # Production install packages
    make pipenv-prod
    # Production compile all
    make compileall
    ;;
  db_c)
    rm -f data/dcr.db
    pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}"
    ;;
  all|p_i)
    rm -rf data/inbox
    mkdir data/inbox
    cp -r tests/inbox/* data/inbox
    pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}"
    ;;
  *)
    echo "Usage: ./run_test.sh all | db_c | m_d | m_p | p_i | p_2_i"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
