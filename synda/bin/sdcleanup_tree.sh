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
#   -
#       "-r" option of xargs prevents the following msg to show when no empty dir exists in the tree
#       <---
#       rmdir: missing operand
#       Try `rmdir --help' for more information.
#       --->
#   - "+e" option is used here to inhibit rmdir error.
#       - rmdir error happens for example in the following case:
#           - rpm package based installation
#           - openid set, but CMIP5 role missing
#           - sudo synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
#           - file is not downloaded due to missing CMIP5 role
#           - sudo synda remove cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
#           - rmdir error occurs
#       - explanation:
#           - no file exist in the data path when sdcleanup_tree.sh is triggered
#           - rmdir error occurs because after /srv/synda/sdt/.../... (empty) folders are removed,
#             rmdir try to remove "/" folder (root), which raise rmdir error (seems that "/"
#             is handled in a specific way and is not inhibited by --ignore-fail-on-non-empty flag)
#   - subshell is used here to prevent setting "+e" option globally (i.e. for the all script)
#
( set +e ; find -L $data_path -type d -empty | sort -r | xargs -r rmdir --ignore-fail-on-non-empty -p ; exit 0 )

# as the previous command may also remove 'data' folder (when all data have been removed), we re-create 'data' if missing
if [ ! -d $data_path ]; then
    mkdir -p $data_path
fi

msg "INF004" "sdcleanup_tree.sh script stopped"

exit 0
