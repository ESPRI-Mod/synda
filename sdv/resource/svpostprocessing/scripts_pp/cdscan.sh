#!/bin/bash -e

# Description
#   This script apply cdscan cdat-command on a variable,
#   creating xml aggregation for every variable existing in "<ROOT>/esgf/process" tree.
#   Processes by variable.
#
# Notes
#   - trailing slash is mandatory in input
#   - python dependencies : cdat or cdat_lite
#
# Usage
#   ./cdscan.sh <PROJECT> <SCR_PATH> <DEST_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains NetCDF files
#   <SRC_PATH>  : /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>/
#
# Output
#   An atomic dataset full path as the directory that contains XML aggregation files
#   <DEST_PATH> : /prodigfs/project/<PROJECT>/main/<downstream_DRS>/

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
        "--project")            shift; project="${1}"        ;;

        # /prodigfs/esgf/mirror/<PROJECT>/<downstream_DRS>
        "--src_variable_path")  shift; process_path="${1}"    ;;

        # /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>
        "--dest_variable_path") shift; main_path="${1}"   ;;
    esac
    shift
done

xml_output=$( ls ${process_path} | head -1 | sed 's|\_[0-9]*\-[0-9]*\.nc$|\.xml|g' )

export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# --------- main --------- #

msg "INFO" "cdscan.sh started (variable_path = ${process_path})"

umask g+w
mkdir -p ${main_path}
cdscan -x ${main_path}${xml_output} ${process_path}*.nc 1>&2
umask g-w

msg "INFO" "cdscan.sh complete"
