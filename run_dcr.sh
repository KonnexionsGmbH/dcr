#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr.sh: Document Content Recognition.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=d_c_u
export PYTHONPATH=src/dcr

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "all   - Run the complete processing of all new documents"
    echo "d_c_u - Create or upgrade the database"
    echo "m_d_e - Run the development ecosystem"
    echo "m_d_i - Run the installation of the necessary 3rd party packages for development"
    echo "m_p   - Run the installation of the necessary 3rd party packages for production and compile all packages and modules"
    echo "p_i   - Process input folder"
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
  m_d_e)
    # Development ecosystem
    if ! ( make dev_ext ); then
        exit 255
    fi
    ;;
  m_d_i)
    # Development install packages
    if ! ( make inst_dev ); then
        exit 255
    fi
    ;;
  m_p)
    # Development install packages
    if ! ( make inst_prod ); then
        exit 255
    fi
    ;;
  c_p)
    # Production install packages and compile all DCR packages and modules
    if ! ( make prod ); then
        exit 255
    fi
    ;;
  all|d_c_u|p_i)
    if ! ( pipenv run python src/dcr/app.py "${DCR_CHOICE_ACTION}" ); then
        exit 255
    fi
    ;;
  *)
    echo "Usage: ./run_dcr.sh all | d_c_u | m_d_e | m_d_i | m_p | p_i"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
