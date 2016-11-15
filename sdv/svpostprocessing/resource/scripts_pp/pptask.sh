#!/bin/bash -e

# Description
#   This script fake doing some post-processing work
#
# Usage
#   ./pptask.sh

# ------ functions ------ #

curdate ()
{
    date +'%Y/%m/%d %I:%M:%S %p'
}

msg ()
{
    l__code="${1}"
    l__msg="${2}"

    echo "$(curdate) ${l__code} ${l__msg}" 1>&2
}


# --------- arguments & initialization --------- #

while [ "${1}" != "" ]; do
    case "${1}" in
        "--project")            shift; project="${1}"         ;;
        "--src_variable_path")  shift; process_path="${1}"    ;;
        "--dest_variable_path") shift; main_path="${1}"       ;;
    esac
    shift
done


# --------- main --------- #

msg "INFO" "pptask.sh started"

# post-processing task goes here

msg "INFO" "pptask.sh complete"

exit 0
