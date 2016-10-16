#!/bin/bash -e

# Description
#   This script generates ESGF mapfile.
#   Processes by dataset.
#
# Notes
#   - trailing slash is mandatory in input
#
# Usage
#   ./mapfile.sh <PROJECT> <DATASET_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   A dataset full path as the directory that contains hardlinks
#   <DATASET_PATH>
#   /prodigfs/project/<PROJECT>/main/<downstream_DRS>/
#
# Output
#   ESGF mapfile
#   /prodigfs/esgf/mapfile/<PROJECT>/<downstream_DRS>/<DATASET_ID>.map

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

        # /prodigfs/project/<PROJECT>/main/<downstream_DRS>
        "--dataset_path") shift;  dataset_path="${1}"   ;;

        # Path this script is from
        "--script_dir") shift;  scripts_path="${1}"   ;;
    esac
    shift
done


# --------- main --------- #

msg "INFO" "mapfile.sh started (dataset_path = ${dataset_path})"

esgprep mapfile -i ${scripts_path}/config/. --project ${project,,} ${dataset_path} --outdir ${dataset_path%project*}esgf/mapfiles/${project}/pending/. -v

msg "INFO" "mapfile.sh complete"
