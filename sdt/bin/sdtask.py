#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains funcs used in 'sdtaskscheduler' module."""

import sys
import os
import sdapp
import sdconfig
import sdfiledao
import sddao
import sdconst
import sdfilequery
import sdtime
import sdprofiler
import sdppproxy
import sdeventdao
import sdlog
import sddb
import sddeletefile
import sdtrace
from sdexception import NoTransferWaitingException,FatalException,RemoteException
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
            #sdtrace.log_exception()

            raise

@sdprofiler.timeit
def transfers_end():
    """Process end of transfer instructions.
    
    When a task is done, tasks are enqueued. Those tasks are then processed by
    this function.
    """

    dmngr.transfers_end()

def prepare_transfer(tr):

    # we reset values from previous try if any
    tr.end_date=None
    tr.error_msg=None
    tr.status=sdconst.TRANSFER_STATUS_RUNNING
    tr.start_date=sdtime.now()

def pre_transfer_check_list(tr):
    """
    Return:
        Check list status

        True: Check list OK
        False: Check list NOK
    """

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

            return False
        else:
            # file not here, start the download

            return True
    elif lfae_mode=="replace":
        if os.path.isfile(tr.get_full_local_path()):
            sdlog.info("SYNDTASK-187","Local file already exists: remove it (lfae_mode=replace,local_file=%s)"%tr.get_full_local_path())
            os.remove(tr.get_full_local_path())

        return True
    elif lfae_mode=="abort":
        if os.path.isfile(tr.get_full_local_path()):
            sdlog.info("SYNDTASK-188","Local file already exists: transfer aborted (lfae_mode=abort,local_file=%s)"%tr.get_full_local_path())

            tr.status=sdconst.TRANSFER_STATUS_ERROR
            tr.error_msg="Local file already exists: transfer aborted (lfae_mode=abort)"
            tr.end_date=sdtime.now()
            sdfiledao.update_file(tr)

            return False
        else:
            return True

@sdprofiler.timeit
def transfers_begin():
    transfers=[]

    new_transfer_count=max_transfer - sdfilequery.transfer_running_count() # compute how many new transfer can be started
    if new_transfer_count>0:
        for i in range(new_transfer_count):
            try:
                tr=sddao.get_one_waiting_transfer()

                prepare_transfer(tr)

                if pre_transfer_check_list(tr):
                    sdfiledao.update_file(tr)
                    transfers.append(tr)
            except NoTransferWaitingException, e:
                pass

    dmngr.transfers_begin(transfers)

def get_download_manager():
    download_manager='globustransfer_dm' if sdconfig.config.getboolean('module','globustransfer') else 'default_dm'

    if download_manager=='globustransfer_dm':
        import sddmgo
        return sddmgo
    elif download_manager=='default_dm':
        import sddmdefault
        return sddmdefault
    else:
        assert False

def can_leave():
    return dmngr.can_leave()

def fatal_exception():
    return dmngr.fatal_exception()

# init.

max_transfer=sdconfig.config.getint('download','max_parallel_download')
lfae_mode=sdconfig.config.get('behaviour','lfae_mode')

dmngr=get_download_manager()
