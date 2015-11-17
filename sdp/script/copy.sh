#!/bin/bash -e

##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################
 
# Description
#   This script copy variable from 'process' tree to 'merge' tree
#   creating hardlinks in 'merge' tree for every complete variable in 'process' tree
# 
# Notes
#   - the process is incremental ('merge' tree is not removed every night)
#   - CMIP5 project only
#   - trailing slash is mandatory in input
#   - files removed in source are not removed from destination here (this has to be done by suppresion pipeline)
#
# Usage
#   ./copy.sh <path>
#
# Input
#   variable full path (e.g. <PREFIX>/esg/CMIP5/process/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/)
#
# Output
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

while [ "$1" != "" ]; do
    case "$1" in
        "--project")       shift; project="$1"         ;;
        "--variable_path") shift; variable_path="$1"   ;;
    esac
    shift
done

process_path=$variable_path
merge_path=$( echo "${variable_path}" | sed 's|/process/|/merge/|' )

# --------- main --------- #

msg "INF001" "copy.sh started (variable_path = ${variable_path})"

if [ -d ${process_path} ]; then

    # mkdir is needed, because rsync expects destination path to exist (or at least parent folders in destination path). 
    # More info: http://www.schwertly.com/2013/07/forcing-rsync-to-create-a-remote-path-using-rsync-path/
    mkdir -p ${merge_path} 

    # TODO: is '--delete' rsync option necessary in here ?
    /usr/bin/rsync -viax --delete --link-dest=${process_path} ${process_path} ${merge_path}
fi

msg "INF002" "copy.sh complete"
