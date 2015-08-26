#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing routines."""

import re
import argparse
import json
from spexception import SPException,NoPostProcessingTaskWaitingException,PipelineRunningException
from sptypes import JOBRun,PPPRun
import splog
import spdb
import spconst
import sptime
import spppp
import spppprdao
import spjobrdao
import spconfig

def all_variable_complete(dataset_pattern,conn):

    # retrieve pipeline runs
    li=spppprdao.get_pppruns(order='fifo',dataset_pattern=dataset_pattern,pipeline='CMIP5_001',conn=conn)

    for ppprun in li: # loop over the different runs of the same pipeline
        if ppprun.status!=spconst.PPPRUN_STATUS_DONE:
            return False

    return True

def build_ppprun(pipeline,status,project,model,dataset_pattern,variable):
    pipeline=spppp.get_pipeline(pipeline)

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

            # check existing pipeline state (if state do not allow us to restart it, we raise PipelineRunningException)
            if pipeline=='CMIP5_001':
                if ppprun.status==spconst.PPPRUN_STATUS_DONE:
                    pass
                else:
                    raise PipelineRunningException()
            elif pipeline=='CMIP5_002':
                if ppprun.status==spconst.PPPRUN_STATUS_DONE:
                    pass
                elif ppprun.status==spconst.PPPRUN_STATUS_PAUSE:
                    if ppprun.state=='S1100': # be sure we are at the beginning of the pipe (as 'pausing' is a status that may occurs anywhere in the pipeline). TODO: replace hardcoded S1100 with pipeline first state (as state name can change in the future)
                        # note that in this case, we update the pipe, but it doesn't hange anything as the pipe is already in the right state, 
                        pass
                    else:
                        raise PipelineRunningException()
                else:
                    raise PipelineRunningException()
            else:
                raise SPException('SPPOSTPR-450','Unknown pipeline (%s)'%pipeline)

            # retrieve pipeline definition (note that code below is not reentrant/threadsafe: it works only because execution mode is serial (i.e. non parallel))
            pipeline=spppp.get_pipeline(pipeline)
            pipeline.reset()
            state=pipeline.get_current_state().source
            transition=pipeline.get_current_state().transition

            # set new values
            ppprun.state=state
            ppprun.transition=transition.name
            ppprun.status=status
            ppprun.error_msg=None
            ppprun.last_mod_date=sptime.now()

            # save
            spppprdao.update_ppprun(ppprun,conn)
            splog.info("SPPOSTPR-202","Pipeline updated (%s)"%str(ppprun))
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
        pipeline=spppp.get_pipeline(ppprun.pipeline)
        pipeline.set_current_state(ppprun.state)
        folder=pipeline.get_current_state().transition.workdir

        # dataset_pattern resolution (when possible (e.g. for 'merge' it is not possible as we go from TWO src dir (i.e. 'output12'), so we need to keep the '*' char))
        #
        # TODO: find an elegant way to manage /*/ tranformation (i.e. to /process/ for the axis_normal case). Maybe move this logic into spppp.py.
        #
        dataset_pattern=ppprun.dataset_pattern.replace('/*/','/'+folder+'/')

        # prepare argument to make it easier for the job
        if ppprun.variable=='':
            arg='%s/%s/'%(spconfig.data_folder,dataset_pattern)
        else:
            arg='%s/%s/%s/'%(spconfig.data_folder,dataset_pattern,ppprun.variable)

        # notes: 
        #  - job_class and transition are the same (transition is from the finite state machine view, and job_class is from the job consumer view).
        #  - transition must be set the the job, because we need it when doing insertion in jobrun table.
        job=JOBRun(job_class=ppprun.transition,
                full_path_variable=arg, # TODO: rename full_path_variable into generic name (matching both variable and dataset only path)
                error_msg=None,
                transition=ppprun.transition,
                dataset_pattern=dataset_pattern,
                variable=ppprun.variable,
                start_date=sptime.now(),
                ppprun_id=ppprun.ppprun_id,
                project=ppprun.project)

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
        pipeline=spppp.get_pipeline(ppprun.pipeline)
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


        # if all variable 'done', switch dataset pipeline from 'pause' to 'waiting'
        if ppprun.pipeline=='CMIP5_001': # this block must be executed only at the end of CMIP5_001 pipeline
            if ppprun.status==spconst.PPPRUN_STATUS_DONE:
                if all_variable_complete(ppprun.dataset_pattern,conn):
                    li=spppprdao.get_pppruns(order='fifo',dataset_pattern=ppprun.dataset_pattern,pipeline='CMIP5_002',conn=conn)
                    if len(li)==1:
                        dataset_ppprun=li[0]
                        if dataset_ppprun.status==spconst.PPPRUN_STATUS_PAUSE:

                            dataset_ppprun.status=spconst.PPPRUN_STATUS_WAITING
                            dataset_ppprun.last_mod_date=sptime.now()

                            spppprdao.update_ppprun(dataset_ppprun,conn)


        conn.commit()
    finally:
        spdb.disconnect(conn) # if exception occur, we do the rollback here

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
