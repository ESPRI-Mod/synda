#!/bin/bash
##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdstart.sh 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12614 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# This script starts Synchro-data daemon

if [ -z "$ST_HOME" ]; then
    echo "SDASTART-001 - Root directory not found"
    exit 1
fi

source $ST_HOME/bin/sdutils.sh

usage ()
{
    cat >&1 << EOF

USAGE: $(basename $0): [-h]

OPTIONS:
EOF
}

# parse

quiet=0
while getopts 'hq' OPTION
do
    case $OPTION in
        h)	usage
            exit 0
            ;;
        q)	quiet=1
            ;;
        ?)	exit 1 # we come here when a required option argument is missing (bash getopts mecanism)
            ;;
    esac
done
shift $(($OPTIND - 1)) # remove options

# init

export log=${ST_HOME}/log
export bin=${ST_HOME}/bin
export tmp=${ST_HOME}/tmp
daemon_pid_file="$tmp/daemon.pid"

start_daemon

exit 0
