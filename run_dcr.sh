#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr.sh: Document Content Recognition.
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

export LOG_FILE=run_dcr.log
rm -f run_dcr.log
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
    if ! ( make pipenv-dev ); then
        exit 255
    fi
    # Development ecosystem
    if ! ( make dev ); then
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
  all|db_c|p_i|p_2_i)
    if ! ( pipenv run python src/dcr/dcr.py "${DCR_CHOICE_ACTION}" ); then
        exit 255
    fi
    ;;
  *)
    echo "Usage: ./run_dcr.sh all | db_c | m_d | m_p | p_i | p_2_i"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
