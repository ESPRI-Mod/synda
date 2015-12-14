#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module manages automated tasks.

Note
    This module is intended to run in background.
"""

import os
import sys
import time
import sdapp
import sdconfig
import sdwatchdog
import sddao
import sdfiledao
import sdconst
import sdutils
import sdlog
import sdlogon
import sdtask
import sdprofiler
import sdstatquery
from sddownload import Download
from sdexception import FatalException,SDException,CertificateRenewalException

def terminate(signal,frame):
    global quit

    import sdlog

    print # this print is just not to display the msg below on the same line as ^C

    sdlog.info("SDTSCHED-004","Shutdown in progress..",stderr=True)

    if scheduler_state!=1: # we can only stop the scheduler if it is running
        sdlog.info("SDTSCHED-009","The daemon is not running (scheduler_state=%s)"%scheduler_state)
        return

    sdwatchdog.quit=1
    quit=1

    # kill all childs (i.e. abort running transfer(s) if any)
    import psutil
    parent = psutil.Process(os.getpid())

    # NEW WAY
    # see TAG54353543DFDSFD for info
    #
    if hasattr(parent, 'get_children'):
        for child in parent.get_children(True):
            if child.is_running():
                child.terminate()
    else:
        for child in parent.children(True):
            if child.is_running():
                child.terminate()

    # OLD
    """
    for child in parent.get_children(True):
        if child.is_running():
            child.terminate()
    """

def cleanup_running_transfer():
    """This handle zombie cases (transfers with 'running' status, but not running).

    Check for zombie transfer (move "running" transfer to "waiting")
    
    Notes:
        - remaining "running" transfers exist if the daemon has been killed or if the server rebooted when the daemon was running)
        - if there are still transfers in running state, we switch them to waiting and remove file chunk
    """
    transfer_list=sdfiledao.get_files(status=sdconst.TRANSFER_STATUS_RUNNING)

    for t in transfer_list:
        sdlog.info("SDTSCHED-023","fixing transfer status (%s)"%t.get_full_local_path())

        if os.path.isfile(t.get_full_local_path()):
            os.remove(t.get_full_local_path())

        t.status=sdconst.TRANSFER_STATUS_WAITING
        sdfiledao.update_file(t)

def start_watchdog():
    """Starting download processes watchdog."""

    sdlog.info("SDTSCHED-993","Starting watchdog..")

    frozenCheckerThread=sdwatchdog.FrozenDownloadCheckerThread()
    frozenCheckerThread.setDaemon(True)
    frozenCheckerThread.start()

def cleanup():
    # this func is only used in 'nohup' execution mode

    if os.path.isfile(sdconfig.daemon_pid_file):
        os.unlink(sdconfig.daemon_pid_file)

@sdprofiler.timeit
def run_hard_tasks():
    """Hard tasks are executed during application shutdown."""
    global quit

    try:
        sdtask.end_of_tasks()
    except FatalException,e:
        quit=1

@sdprofiler.timeit
def run_soft_tasks():
    """Soft tasks are not executed during application shutdown."""

    if sdconfig.files_download:
        sdtask.start_transfers()

    sdtask.delete_transfers()

    if sdconfig.config.get('daemon','post_processing')=='1':
        sdtask.process_async_event()

@sdprofiler.timeit
def can_leave():
    return sdstatquery.transfer_running_count()==0 and sdtask.eot_queue.empty()

def event_loop():
    global scheduler_state

    sdlog.info("SDTSCHED-533","Connected to %s"%sdconfig.db_file,stderr=True)

    scheduler_state=2
    start_watchdog()
    cleanup_running_transfer()
    scheduler_state=1

    if sdconfig.files_download:

        try:

            if sdlogon.is_openid_set():


                # In this mode, we keep retrying if ESGF IDP is not accessible (e.g. if ESGF is down)
                #
                # Note 
                #     To be practical, a 'systemd reload sdt' command must be implemented
                #     (else, openid change in sdt.conf have no impact until the next
                #     retry, which may be a few hours..). Because currently, synda is not aware
                #     of sdt.conf changes while running.
                #
                #sdlogon.renew_certificate_with_retry(True)
                #sdlogon.renew_certificate_with_retry_highfreq()


                # In this mode, we stop the daemon if ESGF IDP is not accessible (e.g. if ESGF is down)
                #
                sdlogon.renew_certificate(True)


            else:
                sdlog.error("SDTSCHED-928",'OpenID not set in configuration file',stderr=True)
                raise CertificateRenewalException("SDTSCHED-264","OpenID not set in configuration file")

        except SDException,e:
            sdlog.error("SDTSCHED-920","Error occured while retrieving ESGF certificate",stderr=True)
            raise

    sdlog.info("SDTSCHED-902","Transfer daemon is now up and running",stderr=True)

    while True:
        assert os.path.isfile(sdconfig.daemon_pid_file)

        if quit==0:
            run_soft_tasks()

        run_hard_tasks()

        if Download.exception_occurs:
            sdlog.error("SDTSCHED-002","Fatal exception occured in download thread",stderr=True)
            break

        if quit==1:
            if can_leave(): # wait until all threads finish and until everything has been processed on the database I/O queue 
                sdlog.info("SDTSCHED-001","Synda service stopped",stderr=True)
                break

        time.sleep(main_loop_sleep)

    print
    sdlog.info("SDTSCHED-901","Scheduler successfully stopped",stderr=True)

# module init.

quit=0 # 0 => start, 1 => stop
scheduler_state=0 # 0 => stopped, 1 => running, 2 => starting
main_loop_sleep=9
sdlog.set_logger(sdconst.LOGGER_CONSUMER) # use dedicated logger

if sdconfig.prevent_daemon_and_ihm:
    if os.path.isfile(sdconfig.ihm_pid_file):
        sdlog.info("SDTSCHED-014","IHM is running, exiting (%s exists)"%sdconfig.ihm_pid_file,stderr=True)
        sys.exit(1)

if __name__ == '__main__':


    # OLD WAY DAEMON START
    #
    # Code below is for when run in standalone mode (i.e. using nohup instead of python-daemon))
    #
    # Note
    #   In python-daemon mode, signal and daemon pidfile mecanisms are handled by the python-daemon module

    if os.path.isfile(sdconfig.daemon_pid_file):
        sdlog.info("SDTSCHED-012","%s already exists, exiting"%sdconfig.daemon_pid_file,stderr=True)
        sys.exit(1)

    with open(sdconfig.daemon_pid_file, 'w') as fh:
        fh.write(str(os.getpid()))

    import signal
    signal.signal(signal.SIGINT, terminate)   
    signal.signal(signal.SIGTERM, terminate)   

    import atexit
    atexit.register(cleanup) # unexpected exit AND normal exit (during normal exit, cleanup is called twice, that's normal)

    # OLD WAY DAEMON END


    event_loop()

    cleanup() # we also need cleanup here, because when signal occur, atexit is NOT triggered !!!
