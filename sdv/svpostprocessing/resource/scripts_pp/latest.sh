#!/bin/bash -e

# Description
#   This script set "latest" symlinks.
#   Processes by dataset.
#
# Notes
#   - trailing slash is mandatory in input
#
# Usage
#   ./latest.sh <PROJECT> <DATASET_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   A dataset full path as the directory that contains hardlinks
#   <DATASET_PATH>
#   /prodigfs/project/<PROJECT>/main/<downstream_DRS>/
#
# Output
#   The "latest" symlink
#   /prodigfs/project/<PROJECT>/main/<downstream_DRS>/latest -> vYYYYMMDD

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
    esac
    shift
done

dataset_dir=$( dirname ${dataset_path} )
dataset_version=$( basename ${dataset_path} )


# --------- main --------- #

msg "INFO" "latest.sh started (dataset = ${dataset_dir})"

cd ${dataset_dir}

# Unlink existing latest symlink
if [ -h "latest" ]; then
    unlink "latest"
fi

# Set new latest symlink
ln -s ${dataset_version} "latest"

cd - >/dev/null 2>&1

msg "INFO" "latest.sh complete"
