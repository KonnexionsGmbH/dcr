#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr.sh: Document Content Recognition.
#
# ----------------------------------------------------------------------------------

export DCR_CHOICE_ACTION_DEFAULT=c_d

rm -f dcr.log.log

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "c_d             - Compile the development version of dcr"
    echo "c_p             - Compile the productive version of dcr"
    echo "new             - Complete processing of all new documents"
    echo "p_i             - Process input folder"
    echo "p_i_o           - Process input folder OCR"
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the desired action [default: ${DCR_CHOICE_ACTION_DEFAULT}] " DCR_CHOICE_ACTION
    export DCR_CHOICE_ACTION=${DCR_CHOICE_ACTION:-$DCR_CHOICE_ACTION_DEFAULT}
else
    export DCR_CHOICE_ACTION=$1
fi

echo ""
echo "Script $0 is now running"

export LOG_FILE=run_dcr.log

echo ""
echo "You can find the run log in the file $LOG_FILE"
echo ""

exec &> >(tee -i $LOG_FILE) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "dcr - Document Content Recognition."
echo "------------------------------------------------------------------------------"
echo "CHOICE_ACTION : ${DCR_CHOICE_ACTION}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="

case "${DCR_CHOICE_ACTION}" in
  c_d)
    if ! ( make dev ); then
        exit 255
    fi
    ;;
  c_p)
    if ! ( make prod ); then
        exit 255
    fi
    ;;
  p_i|p_i_o)
    if ! ( python src/dcr/dcr.py "${DCR_CHOICE_ACTION}" ); then
        exit 255
    fi
    ;;
  *)
    echo "Usage: ./run_dcr.sh c_d | c_p | new | p_i | p_i_o"
    ;;
esac

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
