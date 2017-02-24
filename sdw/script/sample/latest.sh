#!/bin/bash -e
##################################
#  @program        synda
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# Description
#   This script set 'latest' symlinks,
#
# Notes
#   - CMIP5 project only
#   - trailing slash is mandatory in input
#   - time to run <= 1min
#   - obs4MIPs is excluded for now (this script only works with GeoMIP and CMIP5)
#
# Usage
#   ./latest.sh <path> 
#
# Input
#   dataset full path (e.g. <PREFIX>/esg/CMIP5/merge/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/)
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

while [ "$1" != "" ]; do
    case "$1" in
        "--project")      shift;  project="$1"        ;;
        "--dataset_path") shift;  dataset_path="$1"   ;;
    esac
    shift
done

dataset_dir=$( dirname $dataset_path)
dataset_version=$( basename $dataset_path )


# --------- main --------- #

msg "INFO" "latest.sh started (dataset_path = ${dataset_path}"

cd "${dataset_dir}"

# Unlink existing latest symlink
if [ -h "latest" ] ; then
    unlink "latest"
fi

# latest symlink
ln -s "${dataset_version}" "latest"

cd - >/dev/null 2>&1

msg "INFO" "latest.sh complete"
