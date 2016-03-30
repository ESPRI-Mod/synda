#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains daemon related operations.

Usage
    pip install python-daemon # note that this will also install 'lockfile' dependency

Note
    This module don't import sdapp on purpose (it will be done in 'sdtaskscheduler').
    If we do import it and it's loaded before the double-fork, then the who_am_i()
    func doesn't work anymore. My understanding is that a double-fork is not like
    an exec, i.e. loaded module before the double fork are reused after the double fork.
    I think that, because it's seems that sdapp module init code doesn't get executed 
    twice (TO BE CONFIRMED).
"""

import os
import grp
import pwd
import time
import daemon
import daemon.pidfile
import traceback
import argparse
import signal
import subprocess
#import sdapp # do no uncomment this (see note above)
import sdconfig
import sdutils
import sdtools
import sdfilepermission
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

def main_loop():
    import sdlog, sdtaskscheduler # both must be here because of double-fork (sdtaskscheduler too, because sdtaskscheduler do use sdlog)
    import sddb # this is to create database objects if not done already

    sdlog.info('SDDAEMON-001',"Daemon starting ...")

    try:
        sdtaskscheduler.event_loop()
    except SDException, e:
        level=sdconfig.config.get('log','verbosity_level')

        if level=='debug':
            # We log everything in debug mode no matter the exception type

            sdlog.debug('SDDAEMON-008',"Exception occured (%s)"%str(e))
        else:
            if isinstance(e,SDException):
                # In this case, we only print the exception code, as the errmsg
                # is likely to be there already (i.e. low-level func should have 
                # log information about this exception).
                # The primary reason for this is to have a clear log entry
                # when authentication failed (e.g. ESGF is down or openid is incorrect)

                sdlog.info('SDDAEMON-010',"Exception occured (%s)"%str(e.code))
            else:
                # This case should not occur, so we log everything to help debugging

                sdlog.info('SDDAEMON-012',"Exception occured (%s)"%str(e))

    sdlog.info('SDDAEMON-034',"Daemon stopped")

def start():

    if not sdutils.is_granted():
        print 'You need to be root to perform this command.'
        return

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

    if not sdutils.is_granted():
        print 'You need to be root to perform this command.'
        return

    if is_running():
        os.kill(pidfile.read_pid(),signal.SIGTERM)
    else:
        print 'Daemon is already stopped.'

def terminate(signum, frame):
    import sdtaskscheduler # must be here because of double-fork (i.e. we can't move import at the top of this file, because the first import must occur in 'main_loop' func).
    sdtaskscheduler.terminate(signum, frame)

def setuid(user,group,context):
    # retrieve numeric uid/gid
    uid=pwd.getpwnam(user).pw_uid
    gid=grp.getgrnam(group).gr_gid

    # be sure file permission works for unprivileged user
    sdfilepermission.run(uid,gid)

    # set_daemon process identity
    context.uid = uid
    context.gid = gid

# init.

pidfile=daemon.pidfile.PIDLockFile(sdconfig.daemon_pid_file)
context=daemon.DaemonContext(working_directory=sdconfig.tmp_folder, pidfile=pidfile,)
context.signal_map={ signal.SIGTERM: terminate, }


# run daemon as unprivileged user (if run as root and unprivileged user set in configuration file)

if sdtools.is_root():

    # retrieve user from configuration file
    user=sdconfig.config.get('daemon','user')
    group=sdconfig.config.get('daemon','group')

    if user and group:

        setuid(user,group,context)

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
