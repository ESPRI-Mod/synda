#!/bin/bash -e

##################################
#  @program        synda
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# Description
#   scan repository and remove empty files and empty directories
#
# Usage
#   ./sdcleanup_tree.sh

# --------- func --------- #

curdate ()
{
    date '+%F %T'
}

msg ()
{
	l__code="$1"
	l__msg="$2"

	echo "$(curdate) - ${0##*/} - $l__code - $l__msg"
}

# --------- check -------- #

if (( $# != 1 )); then
    msg "ERR001" "Illegal number of parameters"
    exit 1
fi

# --------- init --------- #

PATH=/usr/bin:/bin
data_path="$1"
export LANG=C

# --------- check -------- #

if [ ! -d "$data_path" ]; then
    msg "ERR002" "Incorrect argument"
    exit 1
fi

# --------- main --------- #

msg "INF003" "sdcleanup_tree.sh script started on $data_path"

# remove empty files first
find $data_path -type f -empty -delete

# Remove empty directories starting from leaves of the directory tree (-p option from rmdir)
#
# notes
#   "-r" option of xargs prevents the following msg to show when no empty dir exists in the tree
#   <---
#   rmdir: missing operand
#   Try `rmdir --help' for more information.
#   --->
#
find $data_path -type d -empty | sort -r | xargs -r rmdir --ignore-fail-on-non-empty -p

# as the previous command may also remove 'data' folder (when all data have been removed), we re-create 'data' if missing
if [ ! -d $data_path ]; then
    mkdir $data_path
fi

msg "INF004" "sdcleanup_tree.sh script stopped"

exit 0
