#!/usr/share/python/synda/sdt/bin/python
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
    This module don't import sdapp on purpose (it will be done after the
    'double-fork'). If we do import it and it's loaded before the
    double-fork, then who_am_i() doesn't work anymore. i.e. sdapp module init
    code doesn't get executed twice. TAGJL54JJJ3JK22LLL.
"""

import os
import sys
import grp
import pwd
import time
import daemon
import daemon.pidfile
import psutil
import argparse
import signal
import subprocess
#import sdapp # do no uncomment this (see note above)
import sdconfig
import sdutils
import sdtools
import sdpermission
#import sdfilepermission
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
    import sdapp, sdlog, sdtaskscheduler # must be here because of double-fork
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

def test_write_access(file_):
    if os.path.isfile(file_):
        sys.stderr.write('Cannot perform write test: file already exists (%s)\n'%file_)
        sys.exit(1) # FIXME: move exit() call upstream
    if user and group:
        uid=pwd.getpwnam(user).pw_uid
        gid=grp.getgrnam(group).gr_gid
        os.setgid(gid)
        os.setuid(uid)
    with open(file_,'w') as fh:
        fh.write('write test\n')
        os.unlink(file_)
    sys.stderr.write('Write test successfully completed (%s)\n'%file_)

def start():

    # run daemon as unprivileged user (if run as root and unprivileged user set in configuration file)
    if sdtools.is_root():
        if user and group:
            unprivileged_user_mode()

    if not is_running():
        try:
            with context:
                main_loop()
        except Exception, e:
            import sdtrace
            sdtrace.log_exception()





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

        pid=pidfile.read_pid()

        if psutil.pid_exists(pid):
            os.kill(pid,signal.SIGTERM)
        else:
            import sdlog # sdlog import must not be at the top of this file, because of double-fork

            sdlog.error('SDDAEMON-014',"Warning: daemon pidfile exists but daemon process doesn't exist. Most often, this is caused by an unexpected system restart (e.g. kernel panic).")

            # remove orphan pidfile
            sdlog.info('SDDAEMON-016',"Removing orphan daemon pidfile (%s)."%sdconfig.daemon_pid_file)
            os.unlink(sdconfig.daemon_pid_file)
 
    else:
        sdtools.print_stderr('Daemon is already stopped.')

def terminate(signum, frame):
    import sdtaskscheduler # must be here because of double-fork (i.e. we can't move import at the top of this file, because the first import must occur in 'main_loop' func).
    sdtaskscheduler.terminate(signum, frame)

def unprivileged_user_mode():
    # retrieve numeric uid/gid
    uid=pwd.getpwnam(user).pw_uid
    gid=grp.getgrnam(group).gr_gid

    # be sure file permission works for unprivileged user
    #
    # shouldn't be needed anymore as this is now handled externaly
    # (after installation, all synda files are group-writable and belongs to
    # the synda group).
    #
    #sdfilepermission.run(uid,gid)

    # set_daemon process identity
    context.uid = uid
    context.gid = gid

    # enable support for supplementary group
    #
    # (depends on Python 2.7+ and python-daemon 2.1.1+)
    #
    context.initgroups=True

# init.

os.umask(0002)

pidfile=daemon.pidfile.PIDLockFile(sdconfig.daemon_pid_file)
context=daemon.DaemonContext(working_directory=sdconfig.tmp_folder, pidfile=pidfile,)
context.signal_map={ signal.SIGTERM: terminate, }

# retrieve unprivileged user from configuration file if any
user=sdconfig.config.get('daemon','user')
group=sdconfig.config.get('daemon','group')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    args = parser.parse_args()

    if args.action in ['start','stop']:
        if not sdpermission.is_admin():
            sdtools.print_stderr() # this is to prevent having all on the same line when using "synda service" command e.g. "Shutting down synda daemon (sdt): You need to be root to perform this command."
            sdtools.print_stderr(sdi18n.m0027)
            sys.exit(1)

    if args.action == 'start':
        start()

        #time.sleep(18) # can take some time to start
        #
        #if not is_running():
        #    import sdlog
        #    sdlog.error("SDDAEMON-222" "Error occurs during transfer daemon startup, see log files for details",stderr=True)
        #    sys.exit(2)

    elif args.action == 'stop':
        stop()
    elif args.action == 'status':
        print get_daemon_status()
    elif args.action == 'test':
        test_write_access('/var/tmp/synda/sdt/daemon.pid')
    else:
        print 'Incorrect argument'
