#!/bin/bash -e

##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: coalesce.sh 2609 2013-04-01 14:52:34Z jripsl $
#  @version        $Rev: 2609 $
#  @lastrevision   $Date: 2013-04-01 16:52:34 +0200 (Mon, 01 Apr 2013) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################
 
# This script merge 'output12' tree into 'process' tree for one variable
#
# Description
#   create hardlinks in "process" tree for every "output[12]" files
#
# Notes
#  - the process is incremental ("process" tree is not removed every night)
#  - CMIP5 project only
#  - files removed in source are not removed from dest here (this is done in "cleanup.sh" script)
#  -
#    rsync "--delete" can't be used, as we merge TWO directory into one
#    (i.e. '--delete' only work with one directory mirroring one directory..)
#  - trailing slash is mandatory in input
#
# Usage
#  ./coalesce.sh 
# 
# Input
#  variable full path with wildcard (e.g. <PREFIX>/esg/CMIP5/*/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/clt/)
#
# Output
#  none
#
# TODO
#  Figure out how to handle case when when a file exists in both source directory 
#  (i.e. which one is kept, do we need to raise an ESGF issue on the mailing list, how to handle deletion (i.e. see TAG422342 tag in memo) etc..)

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

# args

variable_path="$1"

# init
l__project=CMIP5 # currently, only manage CMIP5 project. TODO: this script needs to be modified to manage GeoMIP and other project also !
l__root=/prodigfs/esg
output1_path=$( echo "$variable_path" | sed 's|/\*/|/output1/|' )
output2_path=$( echo "$variable_path" | sed 's|/\*/|/output2/|' )
process_path=$( echo "$variable_path" | sed 's|/\*/|/process/|' )

# --------- main --------- #

msg "INF001" "coalesce.sh script started (variable=$variable_path)"

# This is needed, because rsync expects destination path to exist (or at least parent folders in destination path).
# More info: http://www.schwertly.com/2013/07/forcing-rsync-to-create-a-remote-path-using-rsync-path/
if [ -d $output1_path -o -d $output2_path ]; then
    umask g+w
    mkdir -p $process_path
    umask g-w
fi

if [ -d $output1_path -a -d $output2_path ]; then

    nbr=$( comm -12  <(ls $output1_path | sort ) <(ls $output2_path | sort ) | wc -l ) # list files that intersect
    if [ $nbr -gt 0 ]; then
        # duplicate(s) found

        msg "INF003" "$nbr duplicate(s) found b/w output1 and output2 ($variable_path)"

        # notify computing/modeling center
        # TODO

        # merge using ln as this case is difficult to solve with rsync (rsync copy file instead of linking when file exists in destination (maybe lustre specific))
        cd $process_path
        for f in $( ls $output1_path ); do
            ln ${output1_path}${f} $f
        done
        for f in $( comm -13  <(ls $output1_path | sort ) <(ls $output2_path | sort ) ); do # list files that exist in output2 only
            ln ${output2_path}${f} $f
        done
    else
        if [ -d $output1_path ]; then
            /usr/bin/rsync -viax --link-dest=$output1_path $output1_path $process_path
        fi

        if [ -d $output2_path ]; then
            /usr/bin/rsync -viax --link-dest=$output2_path $output2_path $process_path
        fi
    fi
else
    if [ -d $output1_path ]; then
        /usr/bin/rsync -viax --link-dest=$output1_path $output1_path $process_path
    fi

    if [ -d $output2_path ]; then
        /usr/bin/rsync -viax --link-dest=$output2_path $output2_path $process_path
    fi
fi


msg "INF002" "coalesce.sh script ends."
