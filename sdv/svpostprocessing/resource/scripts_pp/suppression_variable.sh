#!/bin/bash -e

# Description
#   This script removes the atomic dataset from "<ROOT>/esgf/process" output directory.
#   Processes by variable.
#
# Notes
#   - trailing slash is mandatory in input
#
# Usage
#   ./suppression_variable.sh <PROJECT> <VARIABLE_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains NetCDF files
#   <VARIABLE_PATH>
#   /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>/
#
# Output
#   None

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
        # Project ID/Facet
        "--project")       shift; project="${1}"         ;;

        # /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>/
        "--variable_path") shift; variable_path="${1}"   ;;
    esac
    shift
done

# Check path
if [ -z ${variable_path} ]; then
    msg "ERROR" "Incorrect argument"
    exit 1
fi

# Check project
if [ -z ${project} ]; then
    msg "ERROR" "Incorrect argument"
    exit 1
fi


# --------- main --------- #

msg "INFO" "suppression_variable.sh started (variable_path = ${variable_path})"

if [ -d ${variable_path} ]; then
    # Remove variable files
    find ${variable_path} -mindepth 1 -maxdepth 1 -type f -delete 2>&1

    # Remove parent directory and upstream DRS if empty
    rmdir -p ${variable_path} --ignore-fail-on-non-empty
fi

msg "INFO" "suppression_variable.sh complete"
