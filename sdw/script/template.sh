#!/bin/bash -e

##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# Description: Synda post-processing script template
 
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
        "--dataset_pattern")            shift; dataset_pattern="$1"      ;;
        "--variable")                   shift; variable="$1"             ;;
        "--project")                    shift; project="$1"              ;;
        "--model")                      shift; model="$1"                ;;
        "--data_folder")                shift; data_folder="$1"          ;;
    esac
    shift
done

# init

scriptname=${0##*/}

# main

msg "INF001" "$scriptname script started"

msg "INF002" "dataset_pattern: $dataset_pattern"

msg "INF003" "$scriptname script ends."
