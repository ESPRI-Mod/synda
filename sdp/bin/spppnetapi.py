#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains Post-Processing routines available as web service.

Notes
    - 'spppnetapi' means 'Synchro-Data Post-Processing Network API'
    - This module wraps post-processing methods and makes sure
      methods arguments are serializable.
"""

import argparse
import sppostprocessing
from sptypes import JOBRun,Event
import splog
import speventdao
import spdb

def test1(a, b):
    return  {'t':[4,5,6],'sum':a+b}

def test2(a=12, b=14):
    return  {'a':a,'b':b}

def get_job(job_class=None,pipeline=None,order=None):
    job=sppostprocessing.get_job(job_class=job_class,pipeline=pipeline,order=order)

    # debug
    #splog.info('SPPPNEAP-010',"(job=%s)"%str(job.__dict__))

    if job is not None:
        return { 'job':job.__dict__ } # transform job object to dict (needed, because custom class cannot be serialized to JSON)
    else:
        # no more job to process

        return { 'job':None } # 'None' mean no more job to process (note that None is now valid JSON (see rfc7158))

def job_done(job):
    sppostprocessing.job_done(JOBRun(**job))
    response={"error_code":0}
    return response

def event(events):
    # this func is called when new events are coming from Synchro-Data Transfer module

    # debug
    #splog.info('SPPPNEAP-001',"event() method called (args=%s)"%str(events))

    # Deserialize (dict to custom class)
    li=[]
    for e in events:
        event=Event(**e)
        li.append(event)

    speventdao.add_events(li)

    response={"error_code":0}
    return response

class PostProcessingNetAPI():
    methods = {
        "test1": test1,
        "test2": test2,
        "get_job": get_job,
        "job_done": job_done,
        "event": event
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
