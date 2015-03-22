#!/bin/bash
##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdstop.sh 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12614 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# This script stops Synchro-data daemon

if [ -z "$ST_HOME" ]; then
    echo "SDATSTOP-ERR001 - Root directory not found"
    exit 1
fi

source $ST_HOME/bin/sdutils.sh

usage ()
{
	cat >&1 << EOF

USAGE: $(basename $0): [ immediate]
EOF
}

# parse

quiet=0
immediate=0
while getopts 'hiq' OPTION
do
    case $OPTION in
        h)	usage
            exit 0
            ;;
        i)	immediate=1
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

# main

if is_daemon_stopped; then
    msg "SDATSTOP-INF016" "Daemon is already stopped"
    exit 0
fi

if [ $immediate = "0" ]; then
	# in this mode, we wait for download to complete

	msg "SDATSTOP-INF011" "Waiting for running transfer(s) to complete.."
	stop_transfer_daemon # blocking call
	sleep 3
	msg "SDATSTOP-INF002" "Daemon stopped successfully."
elif [ $immediate = "1" ]; then
	# in this mode, we don't wait for download to complete but we wait for "eot_queue" to complete

	stop_transfer_daemon_immediate # blocking call
    sleep 4
	msg "SDATSTOP-INF523" "Daemon stopped"
fi

exit 0
