#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: speventthread.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains events consumer thread."""

import threading
import time
import traceback
import splog
import speventdao
import spconfig
import spconst
import spdb
import sppostprocessing
import spppp
from spexception import SPException,PipelineRunningException

def create_pipeline(pipeline,status,e,conn):
    try:
        sppostprocessing.add_ppprun(pipeline,status,e.project,e.model,e.dataset_pattern,e.variable,conn)
        e.status=spconst.EVENT_STATUS_OLD # mark events as done
    except PipelineRunningException, ex: # keep exception instance name as 'ex' not to collide with 'e' event name
        splog.warning('SPEVENTT-012',"Event status set to anomaly")
        e.status=spconst.EVENT_STATUS_ANOMALY # mark events as anomaly (this event has been inhibited and may need to be manually switched to 'new'. also most often it's not necessary (i.e. it has been inhibited because another identical event was preceding it))

def process_event(e,conn):
    if e.name==spconst.EVENT_OUTPUT12_VARIABLE_COMPLETE:
        pipeline='CMIP5_001'
        create_pipeline(pipeline,spconst.PPPRUN_STATUS_WAITING,e,conn)

    elif e.name==spconst.EVENT_OUTPUT12_LATEST_DATASET_COMPLETE:
        pipeline='CMIP5_002'
        assert e.variable == ''
        create_pipeline(pipeline,spconst.PPPRUN_STATUS_PAUSE,e,conn)

    elif e.name==spconst.EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE:

        # not implemented yet
        raise SPException("SPEVENTT-006","Unsupported event (%s)"%str(e))

        #pipeline='CMIP5_003'
        #assert e.variable == ''
        #create_pipeline(pipeline,spconst.PPPRUN_STATUS_PAUSE,e,conn)

    else:
        raise SPException("SPEVENTT-004","Unsupported event (%s)"%str(e))

def consume_events():
    try:
        events=speventdao.get_events(status=spconst.EVENT_STATUS_NEW,limit=20) # process 20 events at a time (arbitrary)
        if len(events)>0:
            try:
                conn=spdb.connect()
                conn.execute('begin immediate') # transaction begin (full db lock)

                for e in events:
                    process_event(e,conn)

                # Check
                # (at this point, all events statuses should be !EVENT_STATUS_NEW)
                li=[e for e in events if e.status in [spconst.EVENT_STATUS_NEW]]
                assert len(li)==0
                
                # Switch processed events status in DB
                splog.info('SPEVENTT-003',"%i event(s) processed"%len(events))
                speventdao.update_events(events,conn)

                conn.commit() # transaction end
            finally:
                spdb.disconnect(conn) # if exception occur, we do the rollback here

    except Exception, e:
        traceback.print_exc(file=open(spconfig.stacktrace_log_file,"a"))

def events_loop(stop_event):
    while not stop_event.is_set():
        consume_events()
        time.sleep(10)

def start():
    splog.info('SPEVENTT-001',"Event thread starting ...")
    event_thread.start()

def stop():
    splog.info('SPEVENTT-002',"Event thread stopping ...")
    stop_event.set()
    event_thread.join()

# init.

stop_event=threading.Event()
event_thread=threading.Thread(name='event_thread', target=events_loop, args=(stop_event,))
