#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synchro-data
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains events used in 'sdtaskscheduler' module."""

import sys
import os
import time
import Queue
import traceback
import sdconfig
import sdfiledao
import sdconst
import sdstatquery
import sdtime
import sdprofiler
import sdppproxy
import sdeventdao
import sdlog
import sddb
import sddeletefile
from sddownload import Download,end_of_transfer
from sdexception import NoTransferWaitingException,FatalException,RemoteException
from sdworkerutils import WorkerThread
from sdtypes import File

@sdprofiler.timeit
def delete_transfers():
    sddeletefile.delete_transfers(limit=100)

@sdprofiler.timeit
def process_async_event(): # 'async' is because event are waiting in 'event' table before being proceeded
    events=sdeventdao.get_events(status=sdconst.EVENT_STATUS_NEW,limit=200) # process 200 events at a time (arbitrary)

    if len(events)>0:

        try:
            sdppproxy.event(events)

            for e in events:
                e.status=sdconst.EVENT_STATUS_OLD

            sdeventdao.update_events(events,commit=False)
            sddb.conn.commit()
            sdlog.info("SYNDTASK-001","Events status succesfully updated")
        except RemoteException,e: # non-fatal
            sddb.conn.rollback()
            sdlog.info("SYNDTASK-002","Error occurs during event processing (%s)"%str(e))
        except Exception,e: # fatal
            sddb.conn.rollback()
            sdlog.error("SYNDTASK-018","Fatal error occurs during event processing (%s)"%str(e))

            # debug
            #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))

            raise

@sdprofiler.timeit
def end_of_tasks():
    """When a task is done, DB orders are enqueued. Those orders are then executed in this function."""

    for i in range(8): # arbitrary
        try:
            task=eot_queue.get_nowait() # raises Empty when empty
            end_of_transfer(task)
            eot_queue.task_done()
        except Queue.Empty, e:
            pass
        except FatalException, e:
            raise
        except:

            # debug
            #traceback.print_exc(file=sys.stderr)
            #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))

            raise

@sdprofiler.timeit
def start_transfers():
    def start_transfer(tr):
        """Retrieve next transfer to start
        
        Note
            if no more transfer waiting, get_transfer() raises "NoTransferWaitingException" exception
        """
        def start_transfer_thread(tr):
            sdfiledao.update_file(tr)
            th=WorkerThread(tr,eot_queue,Download)
            th.setDaemon(True) # if main thread quits, we kill running threads (note though that forked child processes are NOT killed and continue running after that !)
            th.start()


        # we reset values from previous try if any
        tr.end_date=None
        tr.error_msg=None
        tr.status=sdconst.TRANSFER_STATUS_RUNNING
        tr.start_date=sdtime.now()

        if lfae_mode=="keep":
            # usefull mode if
            #  - metadata needs to be regenerated without retransfering the data
            #  - synda files are mixed with files from other sources

            if os.path.isfile(tr.get_full_local_path()):
                # file already here, mark the file as done

                sdlog.info("SYNDTASK-197","Local file already exists: keep it (lfae_mode=keep,local_file=%s)"%tr.get_full_local_path())

                tr.status=sdconst.TRANSFER_STATUS_DONE
                tr.error_msg="Local file already exists: keep it (lfae_mode=keep)"
                tr.end_date=sdtime.now()
                sdfiledao.update_file(tr) # note: it is important not to update a running status in this case, else local file non-related with synda may be removed by synda (because of cleanup_running_transfer() func). See mail from Hans Ramthun at 20150331 for more details.
            else:
                # file not here, start the download

                start_transfer_thread(tr)
        elif lfae_mode=="replace":
            if os.path.isfile(tr.get_full_local_path()):
                sdlog.info("SYNDTASK-187","Local file already exists: remove it (lfae_mode=replace,local_file=%s)"%tr.get_full_local_path())
                os.remove(tr.get_full_local_path())

            start_transfer_thread(tr)
        elif lfae_mode=="abort":
            if os.path.isfile(tr.get_full_local_path()):
                tr.status=sdconst.TRANSFER_STATUS_ERROR
                tr.error_msg="Local file already exists: transfer aborted (lfae_mode=abort)"
                tr.end_date=sdtime.now()
                sdfiledao.update_file(tr)
            else:
                start_transfer_thread(tr)


    new_transfer_count=max_transfer - sdstatquery.transfer_running_count() # compute how many new transfer can be started
    if new_transfer_count>0:
        for i in range(new_transfer_count):
            try:
                tr=sdfiledao.get_one_waiting_transfer()
                start_transfer(tr)
            except NoTransferWaitingException, e:
                pass

            time.sleep(1) # this sleep is not to be too agressive with datanodes

# init.

eot_queue=Queue.Queue() # eot means "End Of Task"
max_transfer=sdconfig.config.getint('daemon','max_parallel_download')
lfae_mode=sdconfig.config.get('behaviour','lfae_mode')
