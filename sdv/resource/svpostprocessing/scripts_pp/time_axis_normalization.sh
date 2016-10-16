#!/bin/bash -e

# Description
#   This script checks the time axis of ESGF files in "<ROOT>/esgf/process" directory.
#   Processes by variable.
#
# Notes
#   - trailing slash is mandatory in input
#
# Usage
#   ./time_axis.sh <PROJECT> <VARIABLE_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains hardlinks
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
        "--project")      shift;  project="${1}"        ;;

        # /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>
        "--variable_path") shift;  variable_path="${1}"   ;;

        # Path this script is from
        "--script_dir") shift;  scripts_path="${1}"   ;;
    esac
    shift
done


# --------- main --------- #

msg "INFO" "time_axis_normalization.sh started (variable_path = ${variable_path})"

nctime axis -i ${scripts_path}/config/nctime_config.ini --project ${project} ${variable_path} --write --db --max-threads 1

msg "INFO" "time_axis_normalization.sh complete"
