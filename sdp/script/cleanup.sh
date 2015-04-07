#!/bin/bash -e

##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# Description
#  - scan repository and remove empty files together with empty directories
# Usage
#  - ./cleanup.sh
#

# --------- func --------- #

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

# --------- init --------- #

data_root="/prodigfs/esg/CMIP5"
export LANG=C

msg "CLEANUP-INF003" "Cleanup script started"

cd $data_root

# remove files having a number of links equal to 1 (merge files should have exactly 2 hard links)
# 
# this is typically used when removing old version on IPSLPROD
# (i.e. files are removed by synchro-data from output* tree, but not in merge. 
# files are removed from merge tree with the find command below, 
# which finally release disk space)
#
msg "CLEANUP-INF012" "Delete 'files with links=1' begins"
find merge -type f -links 1 -print -delete
msg "CLEANUP-INF013" "Delete 'files with links=1' ends"

# then remove empty directories starting from leaves of the directory tree (-p option from rmdir)
#
# notes
#   - when using PROC0003 to remove old datasets versions, files are removed in python code, but
#     folders are removed here
#   - "-r" option of xargs prevents the following msg to show when no empty dir exists in the tree
#     <---
#     rmdir: missing operand
#     Try `rmdir --help' for more information.
#     --->
#
#
msg "CLEANUP-INF014" "Delete empty folder begins"
find output[12] merge -type d -empty | sort -r | xargs -r rmdir --ignore-fail-on-non-empty -p
msg "CLEANUP-INF015" "Delete empty folder ends"

# remove dead symlinks
#
# obsolete (latest version should not be removed anymore)
#
#symlinks -rd merge/

msg "CLEANUP-INF004" "Cleanup script stopped ($0)"
