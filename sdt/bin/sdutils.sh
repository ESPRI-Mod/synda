#!/bin/bash
##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# this script contain generic shell funcs

curdate ()
{
    date '+%F %T'
}

msg ()
{
	l__code="$1"
	l__msg="$2"

    logfile=$log/startstop.log

    if [ "$quiet" = "0" ]; then
        ( echo "$(curdate) - $l__code - $l__msg" | tee -a $logfile ) 1>&2  
    else
        echo "$(curdate) - $l__code - $l__msg" >> $logfile
    fi
}

#####################
# return
#  0 running
#  1 not running
is_daemon_running()
{
	if [ -f "$daemon_pid_file" ]; then
		return 0
	else
		return 1
	fi
}

is_daemon_stopped()
{
    ! is_daemon_running
}

#####################
# Returns
#  0: running
#  1: not running
#
# Not used.
#
is_ihm_running ()
{
	if [ -f "$g__synchro_data_IHM_pid_file" ]; then
		return 0
	else
		return 1
	fi
}

#####################
# Returns
#  PID: running
#  "":  not running
get_daemon_PID ()
{
	ps ax | grep -v grep | grep "sdtaskscheduler" | awk '{print $1}'
}

count_running_wget ()
{
	echo $(ps ax | grep wget | grep dev | grep certificate | grep esg | grep directory | grep -v grep | wc -l)
}

start_daemon ()
{
    ( nohup sdtaskscheduler >> $log/nohup.log 2>&1 & )

    msg "START-INF201" "Transfer daemon starting.."

    sleep 18 # can take some time to start

    # check if startup went ok
    is_daemon_running
    if [ $? -ne 0 ]; then
        msg "START-ERR222" "Error occurs during transfer daemon startup, see 'transfer.log' and 'nohup.log' files for details"
        exit 2
    fi

    msg "START-INF204" "Transfer daemon succesfully started"
}

stop_transfer_daemon ()
{
    kill -TERM $(<"$daemon_pid_file")
}

stop_transfer_daemon_immediate ()
{
    pgid=$( ps hp $(<"$daemon_pid_file") -o pgid )  # retrieve gpid
    pgid=$( echo $pgid | sed 's/ //g' )             # trim

    kill -TERM -$pgid                               # ask all the processes of the group to quit (TERM signal is trapped in most scripts)
}
