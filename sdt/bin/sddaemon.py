#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sddaemon.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains daemon related operations.

Usage
    pip install python-daemon # note that this will also install 'lockfile' dependency

Note
    This module don't import sdapp on purpose (it will be done in 'sdtaskscheduler').
    If we do import it and it's loaded before the double-fork, then the who_am_i()
    func doesn't work anymore. My understanding is that a double-fork is not like
    an exec, i.e. loaded module before the double fork are reused after the double fork.
    I think that because it's seems that sdapp module init code doesn't get executed 
    twice (TO BE CONFIRMED).
"""

import os
import time
import daemon
import daemon.pidfile
import traceback
import argparse
import signal
import subprocess
#import sdapp # do no uncomment this (see note above)
import sdconfig
from sdexception import SDException

def get_daemon_status():
    if is_running():
        return "Daemon running"
    else:
        return "Daemon not running"

def print_daemon_status():
    print get_daemon_status()

def is_running():
    if os.path.isfile(sdconfig.daemon_pid_file): # maybe this can be replaced by "pidfile.is_locked()"
        return True
    else:
        return False

# OLD WAY START
"""
def start():
    import sdutils
    (status,stdout,stderr)=sdutils.get_status_output(['%s'%(sdconfig.daemon_start_script),'-q'],preexec_fn=os.setsid) # setsid is to use a different process group (so killing the daemon do not kill interactive session)
    if status!=0:
        raise SDException('SDDAEMON-001',"Daemon failed to start. See log files for details")

def stop():
    import sdutils
    (status,stdout,stderr)=sdutils.get_status_output(['%s'%(sdconfig.daemon_stop_script),'-i','-q'],preexec_fn=os.setsid) # setsid is to use a different process group (so killing the daemon do not kill interactive session)
    if status!=0:
        raise SDException('SDDAEMON-002',"Daemon failed to stop. See log files for details")
"""
# OLD WAY END

# NEW WAY START

def main_loop():
    import sdlog, sdtaskscheduler # both must be here because of double-fork (sdtaskscheduler too, because sdtaskscheduler do use sdlog)
    import sddb # this is to create database objects if not done already

    sdlog.info('SDDAEMON-001',"Daemon starting ...")

    try:
        sdtaskscheduler.event_loop()
    except SDException, e:
        sdlog.info('SDDAEMON-008',"Exception occured (%s)"%str(e))

    sdlog.info('SDDAEMON-034',"Daemon stopped")

def start():
    if not is_running():
        with context:
            try:
                main_loop()
            except Exception, e:
                traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))





        # DOESN'T WORK !
        #
        # BEWARE: tricky code here !!!
        # The idea is after waiting for a while, if daemon startup failed,
        # daemon pid file has been removed by the 'python-daemon' mecanism,
        # thus is_running() should return False in this case.
        #
        """
        time.sleep(5)
        if not is_running():
            print 'Error occurs during daemon startup.'
        """



    else:
        print 'Daemon is already running.'

def stop():
    if is_running():
        os.kill(pidfile.read_pid(),signal.SIGTERM)
    else:
        print 'Daemon is already stopped.'

def terminate(signum, frame):
    import sdtaskscheduler # must be here because of double-fork (i.e. we can't move import at the top of this file, because the first import must occur in 'main_loop' func).
    sdtaskscheduler.terminate(signum, frame)

# init.

pidfile=daemon.pidfile.PIDLockFile(sdconfig.daemon_pid_file)
context=daemon.DaemonContext(working_directory=sdconfig.tmp_folder, pidfile=pidfile,)
context.signal_map={ signal.SIGTERM: terminate, }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    args = parser.parse_args()

    if args.action == 'start':
        start()

        #time.sleep(18) # can take some time to start
        #
        #if not is_running():
        #    import sdlog
        #    sdlog.info("SDDAEMON-222" "Error occurs during transfer daemon startup, see log files for details",stderr=True)
        #    os.exit(2)

    elif args.action == 'stop':
        stop()
    elif args.action == 'status':
        print get_daemon_status()

# NEW WAY END
