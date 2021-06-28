#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.sdt import sdwatchdog
from synda.sdt import sdfiledao
from synda.sdt import sdlog
from synda.sdt import sdlogon
from synda.sdt import sdtask
from synda.sdt import sdfilequery
from synda.sdt import sdsqlutils
from synda.sdt.sdexception import FatalException,SDException,OpenIDNotSetException
from synda.sdt.sdtime import SDTimer

from synda.source.config.file.daemon.models import Config as DaemonFile

from synda.source.config.process.download.constants import TRANSFER

from synda.source.config.file.db.models import Config as DBFile

from synda.source.config.file.user.preferences.decorators import report_elapsed_time_into_log_file
from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.config.file.internal.models import Config as Internal

scheduler_profiling = Preferences().log_scheduler_profiling
DAEMON_FULLFILENAME = DaemonFile().default


def terminate(signal,frame):
    global quit

    from synda.sdt import sdlog

    print()  # this print is just not to display the msg below on the same line as ^C

    sdlog.info("SDTSCHED-004","Shutdown in progress..",stderr=True)

    if scheduler_state!=1: # we can only stop the scheduler if it is running
        sdlog.info("SDTSCHED-009","The daemon is not running (scheduler_state=%s)"%scheduler_state)
        return

    sdwatchdog.quit=1
    quit=1


    # kill all childs (i.e. abort running transfer(s) if any)

    sdlog.info("SDTSCHED-005","Cleanup child processes")

    import psutil
    parent = psutil.Process(os.getpid())

    # see TAG54353543DFDSFD for info regarding this block.
    if hasattr(parent, 'get_children'):
        for child in parent.get_children(True):
            resilient_terminate(child)
    else:
        for child in parent.children(True):
            resilient_terminate(child)


    sdlog.info("SDTSCHED-006","Waiting for the daemon to stop..")

def cleanup_running_transfer():
    """This handle zombie cases (transfers with 'running' status, but not running).

    Check for zombie transfer (move "running" transfer to "waiting")
    
    Notes:
        - remaining "running" transfers exist if the daemon has been killed or if the server rebooted when the daemon was running)
        - if there are still transfers in running state, we switch them to waiting and remove file chunk
    """
    transfer_list=sdfiledao.get_files(status=TRANSFER["status"]['running'])

    for t in transfer_list:
        sdlog.info("SDTSCHED-023","fixing transfer status (%s)"%t.get_full_local_path())

        if os.path.isfile(t.get_full_local_path()):
            os.remove(t.get_full_local_path())

        t.status=TRANSFER["status"]['waiting']
        sdfiledao.update_file(t)

def clear_failed_url():
    """Clears the failed_url table."""
    sdsqlutils.truncate_table("failed_url")

def clear_failed_url_file(filename):
    """Clears the rows of the failed_url table which correspond to one filename."""
    # SQL line "delete from failed_url where col like %/filename"
    sdsqlutils.truncate_part_of_table("failed_url", "url", "%%/%s"%filename )

def resilient_terminate(child):
    """This func terminate the child and inhibits NoSuchProcess exception if any."""

    import psutil

    if child.is_running():
        try:
            child.terminate()
        except psutil.NoSuchProcess as e:
            # this may occurs because of race condition. See TAGGFJDGKDF for more info.

            pass

def start_watchdog():
    """Starting download processes watchdog."""

    sdlog.info("SDTSCHED-993","Starting watchdog..")

    frozenCheckerThread=sdwatchdog.FrozenDownloadCheckerThread()
    frozenCheckerThread.setDaemon(True)
    frozenCheckerThread.start()

def cleanup():
    # this func is only used in 'nohup' execution mode

    if os.path.isfile(DAEMON_FULLFILENAME):
        os.unlink(DAEMON_FULLFILENAME)


@report_elapsed_time_into_log_file(scheduler_profiling)
def run_hard_tasks():
    """Hard tasks are executed during application shutdown."""
    global quit

    try:
        sdtask.transfers_end()
    except FatalException as e:
        quit=1


@report_elapsed_time_into_log_file(scheduler_profiling)
def run_soft_tasks():
    """Soft tasks are not executed during application shutdown."""
    download = Preferences().is_module_download
    if download:
        sdtask.transfers_begin()

    # disabled for now (deletion occurs in realtime in interactive code)
    #sdtask.delete_transfers()


@report_elapsed_time_into_log_file(scheduler_profiling)
def can_leave():
    return sdfilequery.transfer_running_count()==0 and sdtask.can_leave()


def daemon_process():
    # controls
    success = isinstance(DAEMON_FULLFILENAME, str)
    if success:
        success = os.path.isfile(DAEMON_FULLFILENAME)

    if success:
        # process
        if quit == 0:
            run_soft_tasks()

        run_hard_tasks()

        if sdtask.fatal_exception():
            sdlog.error("SDTSCHED-002", "Fatal exception occured during download", stderr=True)
            success = False

        if quit == 1:
            # wait until all threads finish and until everything has been processed on the database I/O queue
            if can_leave():
                sdlog.info("SDTSCHED-001", "eot_queue orders processing completed", stderr=False)
                sdlog.info("SDTSCHED-003", "Running transfer processing completed", stderr=False)
                success = False

    return success


@report_elapsed_time_into_log_file(1)
def event_loop(config_manager):
    global scheduler_state

    credentials = config_manager.get_user_credentials()
    preferences = config_manager.get_user_preferences()

    sdlog.info("SDTSCHED-533", "Connected to %s" % DBFile().get(), stderr=True)

    scheduler_state = 2
    start_watchdog()
    cleanup_running_transfer()
    clear_failed_url()
    if Internal().is_processes_get_files_caching:
        # initializes cache of max priorities
        sdfiledao.highest_waiting_priority(True, True)
    scheduler_state = 1

    if preferences.is_module_download:

        try:

            if credentials.is_openid_set():

                # In this mode, we keep retrying if ESGF IDP is not accessible (e.g. if ESGF is down)
                #
                # Note 
                #     To be practical, a 'systemd reload sdt' command must be implemented
                #     (else, openid change in sdt.conf have no impact until the next
                #     retry, which may be a few hours..). Because currently, synda is not aware
                #     of sdt.conf changes while running.
                #
                #sdlogon.renew_certificate_with_retry(credentials.openid,credentials.password,force_renew_certificate=True)
                #sdlogon.renew_certificate_with_retry_highfreq(credentials.openid,credentials.password,force_renew_certificate=True)

                # In this mode, we stop the daemon if ESGF IDP is not accessible (e.g. if ESGF is down)
                #
                success = sdlogon.renew_certificate(
                    credentials.openid,
                    credentials.password,
                    force_renew_certificate=True,
                )

            else:
                sdlog.error("SDTSCHED-928", 'OpenID not set in configuration file', stderr=True)
                raise OpenIDNotSetException("SDTSCHED-264", "OpenID not set in configuration file")

        except SDException as e:
            sdlog.error("SDTSCHED-920", "Error occured while retrieving ESGF certificate", stderr=True)
            raise

    if success:
        sdlog.info("SDTSCHED-902", "Transfer daemon is now up and running", stderr=True)
        while True:

            evlp0 = SDTimer.get_time()
            assert isinstance(DAEMON_FULLFILENAME, str)
            assert os.path.isfile(DAEMON_FULLFILENAME)

            if quit == 0:
                run_soft_tasks()

            run_hard_tasks()

            if sdtask.fatal_exception():
                sdlog.error("SDTSCHED-002", "Fatal exception occured during download", stderr=True)
                break

            if quit == 1:
                # wait until all threads finish and until everything has been processed on the database I/O queue
                if can_leave():
                    sdlog.info("SDTSCHED-001", "eot_queue orders processing completed", stderr=False)
                    sdlog.info("SDTSCHED-003", "Running transfer processing completed", stderr=False)
                    break

            time.sleep(main_loop_sleep)

            # sdlog.debug("SDTSCHED-400","end of event loop")
            evlp1 = SDTimer.get_elapsed_time(evlp0, show_microseconds=True)
            sdlog.info("SDTSCHED-400", "{} time for once through event loop".format(evlp1))

        print()
        evlp1 = SDTimer.get_elapsed_time(evlp0, show_microseconds=True)
        sdlog.info("SDTSCHED-401", "{} time for once through event loop".format(evlp1))
        sdlog.info("SDTSCHED-901", "Scheduler successfully stopped", stderr=True)

    return success

# module init.

quit=0 # 0 => start, 1 => stopget_openid
scheduler_state=0 # 0 => stopped, 1 => running, 2 => starting
# jfp Previously wwe had main_loop_sleep=9.  1 gives much better throughput if there are many
# parallel downloads.  0 might cause a lot of spinning in low-volume use...
main_loop_sleep=1
sdlog.set_default_logger(Internal().logger_consumer)


if __name__ == '__main__':


    # OLD WAY DAEMON START
    #
    # Code below is for when run in standalone mode (i.e. using nohup instead of python-daemon))
    #
    # Note
    #   In python-daemon mode, signal and daemon pidfile mecanisms are handled by the python-daemon module

    if os.path.isfile(DAEMON_FULLFILENAME):
        sdlog.info("SDTSCHED-012", "{} already exists, exiting".format(DAEMON_FULLFILENAME), stderr=True)
        sys.exit(1)

    with open(DAEMON_FULLFILENAME, 'w') as fh:
        fh.write(str(os.getpid()))

    import signal
    signal.signal(signal.SIGINT, terminate)   
    signal.signal(signal.SIGTERM, terminate)   

    import atexit
    atexit.register(cleanup) # unexpected exit AND normal exit (during normal exit, cleanup is called twice, that's normal)

    # OLD WAY DAEMON END

    event_loop()

    cleanup() # we also need cleanup here, because when signal occur, atexit is NOT triggered !!!
