#!/bin/bash -e

# Description
#   This script remove dataset from 'merge' tree.
#
# Notes
#   - trailing slash is mandatory in input
#   - time to run => <1 mn
#
# Usage
#   ./suppression_merge_if_exists.sh <path>
#
# Input
#   dataset full path (e.g. <PREFIX>/esg/CMIP5/merge/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/)
#
# Output
#   none
#
# TODO
#   none


# --------- func --------- #

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

# check arg
dataset_path=${1}
if [ -z "${dataset_path}" ]; then
    msg "ERR001" "Incorrect arguments"
    exit 1
fi

# check arg depth
slashes_char_count=$( echo $dataset_path | sed 's/[^/]//g' | awk '{ print length }' )
if [ $slashes_char_count -ne 13 ]; then
    msg "ERR002" "Incorrect arguments"
    exit 1
fi

# --------- main --------- #

msg "INFO" "suppression_merge_if_exists.sh started (dataset_path = ${dataset_path})"

if [ -d ${dataset_path} ]; then

    cd ${dataset_path}

    # remove variables files
    find ${dataset_path} -mindepth 2 -maxdepth 2 -type f -delete 2>&1

    # remove variables folders
    rmdir *

    # remove directory
    cd -
    rmdir ${dataset_path}

    # remove dangling symlink
    symlinks -d $(dirname ${dataset_path}) 2>&1

    # remove orphan folder
    rmdir -p $(dirname ${dataset_path}) --ignore-fail-on-non-empty

fi

msg "INFO" "suppression_merge_if_exists.sh complete"
