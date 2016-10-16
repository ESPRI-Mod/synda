#!/bin/bash -e

# Description
#   This script copies an atomic dataset (variable) from "<ROOT>/esgf/process" tree to "<ROOT>/project/<PROJECT>/main"
#   tree creating hardlinks for every complete variable.
#   Processes by variable.
#
# Notes
#   - files removed in source are not removed from destination here (this has to be done by suppresion pipeline)
#   - rsync '--delete' can't be used, as we merge TWO directory into one
#    (i.e. '--delete' only work with one directory mirroring one directory)
#   - trailing slash is mandatory in input
#
# Usage
#   ./copy.sh <PATH> <PROJECT>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains NetCDF files
#   <SRC_PATH>  : /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>/
#
# Output
#   An atomic dataset full path as the directory that contains hardlinks
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
        "--project")            shift; project="${1}"         ;;

        # /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>
        "--src_variable_path")  shift; process_path="${1}"    ;;

        # /prodigfs/project/<PROJECT>/main/<downstream_DRS>
        "--dest_variable_path") shift; main_path="${1}"       ;;
    esac
    shift
done


# --------- main --------- #
msg "INFO" "copy.sh started (variable_path = ${process_path})"

if [ -d ${process_path} ]; then

    # mkdir is needed, because rsync expects destination path to exist (or at least parent folders in destination path).
    # More info: http://www.schwertly.com/2013/07/forcing-rsync-to-create-a-remote-path-using-rsync-path/
    mkdir -p ${main_path}

    /usr/bin/rsync -viax --delete --link-dest=${process_path} ${process_path} ${main_path}
fi

msg "INFO" "copy.sh complete"
