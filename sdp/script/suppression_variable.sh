#!/bin/bash -e

# Description
#  This script remove variable from 'process' tree.
#
# Notes
#  - trailing slash is mandatory in input
#  - time to run => <1 mn
#
# Usage
#  ./suppression_process_if_exists.sh <path>
#
# Input
#  variable full path (e.g. <PREFIX>/esg/CMIP5/process/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/clt/)
#
# Output
#  None

# func

curdate ()
{
     date '+%F %T'
}

msg ()
{
    l__code="$1"
    l__msg="$2"

    echo "$(curdate) - $l__code - $l__msg" 1>&2
}

# args

while [ "$1" != "" ]; do
    case "$1" in
        "--project")       shift; project="$1"         ;;
        "--variable_path") shift; variable_path="$1"   ;;
    esac
    shift
done

# check arg
if [ -z "$variable_path" ]; then
    echo "ERR001 - Incorrect argument"
    exit 1
fi

# check arg depth
#slashes_char_count=$( echo $variable_path | sed 's/[^/]//g' | awk '{ print length }' )
#if [ $slashes_char_count -ne 14 ]; then
#    msg "ERR002" "Incorrect arguments"
#    exit 1
#fi

# main

msg "INF003" "suppression_process_if_exists.sh script started (variable_path=$variable_path)"

if [ -d $variable_path ]; then

    # remove variable files
    find ${variable_path} -mindepth 1 -maxdepth 1 -type f -delete 2>&1

    rmdir -p $variable_path --ignore-fail-on-non-empty
fi

msg "INF004" "suppression_process_if_exists.sh script complete"
