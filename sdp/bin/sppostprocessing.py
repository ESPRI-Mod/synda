#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""Contains post-processing routines."""

import re
import argparse
import json
from bunch import Bunch
from spexception import SPException,NoPostProcessingTaskWaitingException,PipelineRunningException
from sptypes import JOBRun,PPPRun
import sppipelinedep
import splog
import spdb
import spconst
import sptime
import sppipeline
import spppprdao
import spjobrdao
import spconfig

def all_variable_complete(variable_pipeline,dataset_pattern,conn):

    # retrieve pipeline runs
    li=spppprdao.get_pppruns(order='fifo',dataset_pattern=dataset_pattern,pipeline=variable_pipeline,conn=conn)

    for ppprun in li: # loop over the different runs of the same pipeline
        if ppprun.status!=spconst.PPPRUN_STATUS_DONE:
            return False

    return True

def build_ppprun(pipeline,status,project,model,dataset_pattern,variable):
    pipeline=sppipeline.get_pipeline(pipeline)

    # retrieve first pipeline state (note that code below is not reentrant/threadsafe: it works only because execution mode is serial (i.e. non parallel))
    pipeline.reset()
    state=pipeline.get_current_state().source
    transition=pipeline.get_current_state().transition

    # create new pipeline run
    ppprun=PPPRun(  pipeline=pipeline.name,
                    state=state,
                    transition=transition.name,
                    project=project,
                    model=model,
                    priority=spconst.DEFAULT_PRIORITY,
                    crea_date=sptime.now(),
                    status=status,
                    variable=variable,
                    dataset_pattern=dataset_pattern)

    return ppprun

def add_ppprun(pipeline,status,project,model,dataset_pattern,variable,conn):
    if spppprdao.exists_ppprun(PPPRun(pipeline=pipeline,dataset_pattern=dataset_pattern,variable=variable),conn):

        # retrieve pipeline from db
        pppruns=spppprdao.get_pppruns(order='fifo',pipeline=pipeline,dataset_pattern=dataset_pattern,variable=variable,conn=conn)

        if len(pppruns)!=1:
            raise SPException("SPPOSTPR-440","Incorrect number of runs (number_of_runs=%i,pipeline=%s,dataset_pattern=%s,variable=%s)"%(len(pppruns),pipeline,dataset_pattern,variable))
        else:
            ppprun=pppruns[0]

            if ppprun.status in [spconst.PPPRUN_STATUS_PAUSE,spconst.PPPRUN_STATUS_DONE]: # check existing pipeline state (if state do not allow us to restart it, we raise PipelineRunningException). This is to prevent a reset on a running pipeline. 'waiting' is not accepted to prevent race condition (job starting just while we are here) => TBC.
                restart_pipeline(ppprun,status,conn)
            else:
                raise PipelineRunningException()

    else:
        ppprun=build_ppprun(pipeline,status,project,model,dataset_pattern,variable)
        id_=spppprdao.add_ppprun(ppprun,conn) # autoincrement field is stored in 'id_'. Not used for now.
        splog.info('SPPOSTPR-052','New pipeline added (%s,%s,%s,%s,%s,%s)'%(pipeline,status,project,model,dataset_pattern,variable))

def get_job(job_class=None,pipeline=None,order=None): # note that 'job_class' is an alias for 'transition' (seems a better term from the worker view).
    splog.info("SPPOSTPR-108","Job request (job_class=%s,pipeline=%s)"%(job_class,pipeline))

    try:
        conn=spdb.connect()
        conn.execute('begin immediate')

        # get job
        ppprun=spppprdao.get_one_waiting_ppprun(job_class,pipeline,order,conn) # raise exception if no job found

        # retrieve job metadata from pipeline definition
        pipeline=sppipeline.get_pipeline(ppprun.pipeline)
        pipeline.set_current_state(ppprun.state)

        assert pipeline.get_current_state().transition is not None

        generic_args=Bunch(pipeline=ppprun.pipeline,
                           project=ppprun.project,
                           model=ppprun.model,
                           dataset_pattern=ppprun.dataset_pattern,
                           variable=ppprun.variable,
                           data_folder=spconfig.data_folder)

        # notes: 
        #  - job_class and transition are the same (transition is from the finite state machine view, and job_class is from the job consumer view).
        #  - transition must be set in the job, because we need it when doing insertion in jobrun table.
        job=JOBRun(job_class=ppprun.transition,
                args=pipeline.get_current_state().transition.get_args(generic_args),
                error_msg=None,
                transition=ppprun.transition,
                start_date=sptime.now(),
                ppprun_id=ppprun.ppprun_id)

        # update DB
        ppprun.error_msg=None # we reset values from previous try if any
        ppprun.status=spconst.PPPRUN_STATUS_RUNNING
        ppprun.last_mod_date=sptime.now()

        spppprdao.update_ppprun(ppprun,conn)
        conn.commit()

        splog.info("SPPOSTPR-104","Job started (ppprun_id=%s)"%str(job.ppprun_id))

        return job

    except NoPostProcessingTaskWaitingException, e:
        return None # this means no more job to process
    except SPException, e:
        return None # do not return job as error occurs
    finally:
        spdb.disconnect(conn) # MEMO: this also rollback un-commited change

def job_done(job): # note: this method name does not implied that the job complete successfully. It just means the job ended (with or without error).

    # debug
    splog.info("SPPOSTPR-200","DEBUG (%s)"%str(job))

    splog.info("SPPOSTPR-210","Job done (job_class=%s)"%(job.job_class,))

    job.end_date=sptime.now()

    ppprun=spppprdao.get_ppprun(job.ppprun_id)
    assert ppprun.status==spconst.PPPRUN_STATUS_RUNNING

    if job.error==False:
        splog.info("SPPOSTPR-101","Job completed successfully (ppprun_id=%s)"%str(job.ppprun_id))

        job.status=spconst.JOB_STATUS_DONE

        # compute new state
        pipeline=sppipeline.get_pipeline(ppprun.pipeline)
        pipeline.set_current_state(ppprun.state)
        pipeline.next(job.transition_return_code) # as job is done, we move to the next state (next state always exist at this point, else what the point of the job ?)

        # set DAO to new state
        ppprun.state=pipeline.get_current_state().source

        # retrieve the next transition
        next_transition=pipeline.get_current_state().transition

        if next_transition is not None:
            ppprun.transition=next_transition.name
            ppprun.status=spconst.PPPRUN_STATUS_WAITING
        else:
            # if we are here, it means that pipeline is complete

            ppprun.transition=None
            ppprun.status=spconst.PPPRUN_STATUS_DONE

    elif job.error==True:
        splog.info("SPPOSTPR-102","Job failed (ppprun_id=%s)"%str(job.ppprun_id))
        job.status=spconst.JOB_STATUS_ERROR
        ppprun.status=spconst.PPPRUN_STATUS_ERROR
        ppprun.error_msg=job.error_msg

    ppprun.last_mod_date=sptime.now()

    # we also store all job attributes in DB in JSON fmt
    # (some job attributes contain detailed infos of the run, so we keep the all as it may be useful to debug)
    #
    job.runlog=json.dumps(job.__dict__)

    # compute duration
    job.duration=sptime.compute_duration(job.start_date,job.end_date)

    # Update DB
    try:
        conn=spdb.connect()
        spppprdao.update_ppprun(ppprun,conn)
        spjobrdao.add_jobrun(job,conn)

        if ppprun.status==spconst.PPPRUN_STATUS_DONE:
            if ppprun.pipeline in pipelinedep.trigger:
                dependent_pipeline,trigger_type=pipelinedep.trigger[ppprun.pipeline]
                trigger_pipeline(ppprun,dependent_pipeline,trigger_type,conn)

        conn.commit()
    finally:
        spdb.disconnect(conn) # if exception occur, we do the rollback here

def trigger_pipeline(ending,dependent_pipeline,trigger_type,conn): # 'ending' is an alias for the pipeline which just ends
    li=[]

    if trigger_type==spconst.TRIGGER_TYPE_NV2D:
        if all_variable_complete(ending.pipeline,ending.dataset_pattern,conn):
            # all sibling variable pipelines are complete

            # retrieve dataset ppprun
            li=spppprdao.get_pppruns(order='fifo',dataset_pattern=ending.dataset_pattern,pipeline=dependent_pipeline,conn=conn)
        else:
            # some variable pipeline are not complete

            # nothing to do
            pass
    elif trigger_type==spconst.TRIGGER_TYPE_V2V:
        li=spppprdao.get_pppruns(order='fifo',variable=ending.variable,dataset_pattern=ending.dataset_pattern,pipeline=dependent_pipeline,conn=conn)

        if len(li)<1:
            splog.info("SPPOSTPR-264","Dep not found (%s,%s,%s)"%(dependent_pipeline,ending.variable,ending.dataset_pattern))
    elif trigger_type==spconst.TRIGGER_TYPE_D2D:
        li=spppprdao.get_pppruns(order='fifo',dataset_pattern=ending.dataset_pattern,pipeline=dependent_pipeline,conn=conn)

        if len(li)<1:
            splog.info("SPPOSTPR-262","Dep not found (%s,%s)"%(dependent_pipeline,ending.dataset_pattern))
    elif trigger_type==spconst.TRIGGER_TYPE_D2NV:
        li=spppprdao.get_pppruns(order='fifo',dataset_pattern=ending.dataset_pattern,pipeline=dependent_pipeline,conn=conn)

        if len(li)<1:
            splog.info("SPPOSTPR-268","Dep not found (%s,%s)"%(dependent_pipeline,ending.dataset_pattern))
    else:
        splog.info("SPPOSTPR-201","We shouldn't be here (%s,%s)"%(ending.variable,ending.dataset_pattern))


    for ppprun in li:
        pause_to_waiting(ppprun,conn)

def restart_pipeline(ppprun,status,conn):

    # retrieve pipeline definition (note that code below is not reentrant/threadsafe: it works only because execution mode is serial (i.e. non parallel))
    p=sppipeline.get_pipeline(ppprun.pipeline)
    p.reset()
    state=p.get_current_state().source
    transition=p.get_current_state().transition

    # set new values
    ppprun.state=state
    ppprun.transition=transition.name
    ppprun.status=status
    ppprun.error_msg=None
    ppprun.last_mod_date=sptime.now()

    # save
    spppprdao.update_ppprun(ppprun,conn)
    splog.info("SPPOSTPR-202","Pipeline updated (%s)"%str(ppprun))

def pause_to_waiting(ppprun,conn):
    if ppprun.status==spconst.PPPRUN_STATUS_PAUSE:
        ppprun.status=spconst.PPPRUN_STATUS_WAITING
        ppprun.last_mod_date=sptime.now()
        spppprdao.update_ppprun(ppprun,conn)

def is_variable_level_pipeline(ppprun):
    if ppprun.variable=='':
        return False
    else:
        return True

class Execute():
    exception_occurs=False # this flag is used to stop the event loop if exception occurs in thread

    @classmethod
    def run(cls,ppt):
        splog.info("SPPOSTPR-001","Post-processing task started (%s)"%str(ppt))

        cls.start_external_script(ppt) # currently, we only use fork (support for thread without fork (i.e without external process) will be added if needed)

        ppt.end_date=sptime.now()

    @classmethod
    def start_external_script(cls,ppt):
        (status,stdout,stderr)=sputils.get_status_output(ppt.get_command_line(),shell=True) # fork is blocking here, so thread will wait until external process complete
        ppt.script_exit_status=status
        if status==0:
            ppt.status=spconst.JOB_STATUS_DONE

            splog.info("SPPOSTPR-002","Post-processing task successfully completed (%s)"%str(ppt))
        else:
            ppt.status=spconst.JOB_STATUS_ERROR
            ppt.error_msg="Error occurs in external script"

            splog.info("SPPOSTPR-004","Post-processing task completed with error(s) (%s)"%str(ppt))

            # if error occurs in external script, stdout/stderr may contain error messages
            #splog.debug("SPPOSTPR-007","%s"%stderr)
            #splog.debug("SPPOSTPR-008","%s"%stdout)

# init.

pipelinedep=sppipelinedep.get_module()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # test 1
    """
    job=get_job(job_class=['time_axis_normalization'],order='fifo')
    print job
    """

    # test 2
    job=JOBRun(status=spconst.JOB_STATUS_DONE,ppprun_id=1)
    job_done(job)
