#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains daemon related operations.

Note
    This module don't import spapp on purpose (it will be done in 'splog').
    If we do import it and it's loaded before the double-fork, then the who_am_i()
    func doesn't work anymore. My understanding is that a double-fork is not like
    an exec, i.e. loaded module before the double fork are reused after the double fork.
    I think that because it's seems that spapp module init code doesn't get executed 
    twice (TO BE CONFIRMED).
"""

import argparse
import signal
import os
import daemon
import daemon.pidfile
import traceback
import time
#import spapp # do no uncomment this (see note above)
import spconfig
from spexception import SPException

def get_daemon_status():
    if is_running():
        return "Daemon running"
    else:
        return "Daemon not running"

def print_daemon_status():
    print get_daemon_status()

def is_running():
    if os.path.isfile(spconfig.daemon_pid_file): # maybe this can be replaced by "pidfile.is_locked()"
        return True
    else:
        return False

def main_loop():
    import splog, speventthread # both must be here because of double-fork (speventthread too, because speventthread do use splog)

    splog.info('SPDAEMON-001',"Daemon starting ...")

    import spdb # this is to create database objects if not done already (must be done beforee starting the rpc server)

    # start event thread
    if spconfig.config.get('daemon','eventthread')=='1':
        speventthread.start()

    import sprpcserver
    sprpcserver.start()

    # Code below is for a 'while loop' based daemon
    """
    while quit==0:
        splog.info('SPDAEMON-024',"Daemon running")
        time.sleep(3)
    """

    splog.info('SPDAEMON-034',"Daemon stopped")

def start():
    if not is_running():

        # Code below is for a 'while loop' based daemon
        """
        global quit
        quit=0
        """

        with context:
            try:
                main_loop()
            except Exception, e:
                traceback.print_exc(file=open(spconfig.stacktrace_log_file,"a"))

    else:
        print 'Daemon is already running.'

def stop():
    if is_running():
        os.kill(pidfile.read_pid(),signal.SIGTERM)
    else:
        print 'Daemon is already stopped.'

def terminate(signum, frame):
    import splog, speventthread # both must be here because of double-fork (i.e. we can't move import at the top of this file, because the first import must occur in 'main_loop' func). speventthread too, because speventthread do use splog.

    splog.info('SPDAEMON-038',"Daemon stopping ...")

    # stop event thread
    if spconfig.config.get('daemon','eventthread')=='1':
        speventthread.stop()

    # stop HTTP server
    raise SystemExit()

    # Code below is for a 'while loop' based daemon
    """
    global quit
    quit=1
    """

# init.

# quit=0 #  this line is for a 'while loop' based daemon
pidfile=daemon.pidfile.PIDLockFile(spconfig.daemon_pid_file)
context=daemon.DaemonContext(working_directory=spconfig.tmp_folder, pidfile=pidfile,)
context.signal_map={ signal.SIGTERM: terminate, }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    args = parser.parse_args()

    if args.action == 'start':
        start()
    elif args.action == 'stop':
        stop()
    elif args.action == 'status':
        print get_daemon_status()
