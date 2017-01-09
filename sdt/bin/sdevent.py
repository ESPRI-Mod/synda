#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains event related routines."""

import argparse
import logging # we need this to switch log level depending on postprocessing flag
import sdvariable
import sddatasetdao
import sddatasetflag
import sdconfig
import sdproduct
import sdeventdao
import sddao
import sdconst
import sdtime
import sdlog
from sdtools import print_stderr
from sdtypes import Event

""" TODO: add deletion pipeline
def file_deleted_event(d):
    sdlog.log("SYDEVENT-030","'delete_dataset_event' triggered (%s)"%dataset_functional_id,event_triggered_log_level)

    event=Event(name=sdconst.EVENT_OUTPUT12_VARIABLE_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=variable
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
"""

def file_complete_event(tr):
    """
    Note
        when a variable is complete, we know for sure that all variable's files are fetched,
        because a variable is atomic, i.e. it is not possible to retrieve a subset of variable's files
        (this is true because you can't select a subset of the files of a
        variable with the search-API (search-API temporal n spatial filters are
        at variable level without the possibility to ask a subset of the variable's files))
        but a dataset can be marked as complete even if it contains only a subset of variables included in this dataset
        (but still all variables that have been discovered for this dataset must be complete)
    """
    sdlog.log("SYDEVENT-001","'file_complete_event' triggered (%s)"%tr.file_functional_id,event_triggered_log_level)

    if sdconfig.is_event_enabled(sdconst.EVENT_FILE_COMPLETE,tr.project):
        event=Event(name=sdconst.EVENT_FILE_COMPLETE)
        event.project=tr.project
        event.model=tr.model
        event.dataset_pattern=tr.dataset.local_path
        event.variable=tr.variable
        event.filename_pattern=tr.filename
        event.crea_date=sdtime.now()
        event.priority=sdconst.DEFAULT_PRIORITY
        sdeventdao.add_event(event,commit=True)

    # update dataset (all except 'latest' flag)
    tr.dataset.status=sddatasetflag.compute_dataset_status(tr.dataset)
    tr.dataset.last_done_transfer_date=tr.end_date
    sddatasetdao.update_dataset(tr.dataset)

    if sdvariable.is_variable_complete(tr.dataset.dataset_id,tr.variable):
        variable_complete_event(tr.project,tr.model,tr.dataset,tr.variable) # trigger 'variable complete' event

def variable_complete_event(project,model,dataset,variable,commit=True):
    sdlog.log("SYDEVENT-002","'variable_complete_event' triggered (%s,%s)"%(dataset.dataset_functional_id,variable),event_triggered_log_level)

    if sdconfig.is_event_enabled(sdconst.EVENT_VARIABLE_COMPLETE,project):
        event=Event(name=sdconst.EVENT_VARIABLE_COMPLETE)
        event.project=project
        event.model=model
        event.dataset_pattern=dataset.local_path
        event.variable=variable
        event.filename_pattern=''
        event.crea_date=sdtime.now()
        event.priority=sdconst.DEFAULT_PRIORITY
        sdeventdao.add_event(event,commit=commit)

    # cascade 1 (trigger dataset event)
    if dataset.status==sdconst.DATASET_STATUS_COMPLETE:
        dataset_complete_event(project,model,dataset) # trigger 'dataset complete' event

    # cascade 2 (trigger variable output12 event)
    if project=='CMIP5':

        assert '/output/' not in dataset.path

        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset.path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if sdvariable.is_variable_complete(d1.dataset_id,variable) and sdvariable.is_variable_complete(d2.dataset_id,variable):
                dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset.local_path)
                variable_complete_output12_event(project,model,dataset_pattern,variable) # trigger event (cross dataset event)
        else:
            # we also trigger the 'variable_complete_output12_event' event if the variable is over one product only (because if only one product, then output12 event is also true)

            dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset.local_path)
            variable_complete_output12_event(project,model,dataset_pattern,variable) # trigger event (cross dataset event)

def variable_complete_output12_event(project,model,dataset_pattern,variable,commit=True):
    sdlog.log("SYDEVENT-003","'variable_complete_output12_event' triggered (%s,%s)"%(dataset_pattern,variable),event_triggered_log_level)

    event=Event(name=sdconst.EVENT_OUTPUT12_VARIABLE_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=variable
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)

def dataset_complete_event(project,model,dataset,commit=True):
    sdlog.log("SYDEVENT-004","'dataset_complete_event' triggered (%s)"%dataset.dataset_functional_id,event_triggered_log_level)

    # not used for now
    """
    event=Event(name=sdconst.EVENT_DATASET_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
    """

    # <<<--- 'latest' flag management related code begin

    # store current 'latest' flag state
    old_latest=dataset.latest

    # TODO: check if we we switch latest flag independently for each product (meaning output1 latest can be 1 while output2 latest is 0)
    # tag4342342

    # compute new 'latest' flag
    if not old_latest:
        # old state is not latest

        sddatasetflag.update_latest_flag(dataset) # warning: this method modifies the dataset object in memory (and in database too)
    else:
        # nothing to do concerning the 'latest' flag as the current dataset is already the latest
        # (the latest flag can only be switched off (i.e. to False) by *other* datasets versions, not by himself !!!)
        pass

    # store new 'latest' flag state
    new_latest=dataset.latest

    # --->>> 'latest' flag management related code end


    # cascade 1 (trigger dataset latest switch event)
    if (not old_latest) and new_latest:
        # latest flag has been switched from false to true

        dataset_latest_event(project,model,dataset.path,commit=commit) # trigger 'dataset_latest' event


    # cascade 2 (trigger latest dataset complete event)
    if dataset.latest:
        latest_dataset_complete_event(project,model,dataset.local_path,commit=commit)
    else:
        non_latest_dataset_complete_event(project,model,dataset.local_path,commit=commit)


    # cascade 3 (trigger output12 dataset complete event)
    if project=='CMIP5':
        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset.path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if d1.status==sdconst.DATASET_STATUS_COMPLETE and d2.status==sdconst.DATASET_STATUS_COMPLETE:
                dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset.local_path)
                dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)
        else:
            # only one product exists for this dataset

            # not sure if this code is required.
            # basically, it says that if only one product is present (output1 or output2)
            # then the 'output12' is considered ready to be triggered
            # (i.e. output12 does not require output1 and output2 to be present,
            # it only require that if there are, they must both be complete)
            #
            dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset.local_path)
            dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)


    # cascade 4 (trigger latest output12 dataset complete event)
    if project=='CMIP5':
        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset.path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if d1.status==sdconst.DATASET_STATUS_COMPLETE and d2.status==sdconst.DATASET_STATUS_COMPLETE:
                if d1.latest and d2.latest:
                    latest_output12_dataset_complete_event(project,model,dataset_pattern,commit=commit)
                elif not d1.latest and not d2.latest:
                    non_latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)
                else:
                    sdlog.warning("SYDEVENT-032","Event not triggered as one product is latest while the other product is not") # TODO: is this the right way to handle this case ?
        else:
            # only one product exists for this dataset

            # not sure if this code is required.
            # basically, it says that if only one product is present (output1 or output2)
            # then the 'output12' is considered ready to be triggered
            # (i.e. output12 does not require output1 and output2 to be present,
            # it only require that if there are, they must both be complete)
            #
            if dataset.latest:
                latest_output12_dataset_complete_event(project,model,dataset_pattern,commit=commit)
            else:
                non_latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)

def latest_dataset_complete_event(project,model,dataset_pattern,commit=True):
    # this event means latest dataset has been completed (beware: no 'latest switch' event here: was latest before and still is)

    sdlog.log("SYDEVENT-045","'latest_dataset_complete_event' triggered (%s)"%dataset_pattern,event_triggered_log_level)

    if project=='CMIP5':

        # CMIP5 use output12 special event
        return

    if project in sdconst.PROJECT_WITH_ONE_VARIABLE_PER_DATASET:

        # CORDEX and CMIP6 use only variable level event
        return

    event=Event(name=sdconst.EVENT_LATEST_DATASET_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)

def non_latest_dataset_complete_event(project,model,dataset_pattern,commit=True):
    # this event means one non-latest dataset has been completed (beware: no 'latest switch' event here: was not latest before and still isn't)

    sdlog.log("SYDEVENT-048","'non_latest_dataset_complete_event' triggered (%s)"%dataset_pattern,event_triggered_log_level)

    if project!='CMIP5': # CMIP5 use a special event (output12 based)

        # not used for now
        """
        event=Event(name=sdconst.EVENT_NON_LATEST_DATASET_COMPLETE)
        event.project=project
        event.model=model
        event.dataset_pattern=dataset_pattern
        event.variable=''
        event.filename_pattern=''
        event.crea_date=sdtime.now()
        event.priority=sdconst.DEFAULT_PRIORITY
        sdeventdao.add_event(event,commit=commit)
        """

        pass

def dataset_complete_output12_event(project,model,dataset_pattern,commit=True):
    sdlog.log("SYDEVENT-005","'dataset_complete_output12_event' triggered (%s)"%dataset_pattern,event_triggered_log_level)

    # not used
    """
    event=Event(name=sdconst.EVENT_OUTPUT12_DATASET_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
    """

    pass

def latest_output12_dataset_complete_event(project,model,dataset_pattern,commit=True):
    # this event means latest output12 dataset has been completed (beware: no 'latest switch' event here: was latest before and still is)

    sdlog.log("SYDEVENT-006","'latest_output12_dataset_complete_event' triggered (%s)"%dataset_pattern,event_triggered_log_level)

    event=Event(name=sdconst.EVENT_OUTPUT12_LATEST_DATASET_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)

def non_latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=True):
    # this event means one non-latest dataset has been completed (i.e. was not latest before and still isn't)

    sdlog.log("SYDEVENT-007","'non_latest_dataset_complete_output12_event' triggered (%s)"%dataset_pattern,event_triggered_log_level)

    # not used for now
    """
    event=Event(name=sdconst.EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
    """

    pass

def dataset_latest_event(project,model,dataset_path,commit=True):
    # this event means one dataset has been granted latest (i.e. was not latest before and now is)

    sdlog.log("SYDEVENT-008","'dataset_latest_event' triggered (%s)"%dataset_path,event_triggered_log_level)

    # not used for now
    """
    event=Event(name=sdconst.EVENT_DATASET_LATEST)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
    """

    # cascade
    if project=='CMIP5':
        assert '/output/' not in dataset_path

        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset_path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if d1.latest and d2.latest:
                dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset_path)
                output12_dataset_latest_event(project,model,dataset_pattern,commit=commit) # trigger event
        else:
            dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset_path)
            output12_dataset_latest_event(project,model,dataset_pattern,commit=commit) # trigger event

def output12_dataset_latest_event(project,model,dataset_pattern,commit=True):
    # this event means output12 dataset has been granted latest

    sdlog.log("SYDEVENT-009","'output12_dataset_latest_event' triggered (%s)"%dataset_pattern,event_triggered_log_level)

    # not used
    """
    event=Event(name=sdconst.EVENT_OUTPUT12_DATASET_LATEST)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=''
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
    """

# init.

event_triggered_log_level=logging.INFO if sdconfig.config.getboolean('module','post_processing') else logging.DEBUG

if __name__ == '__main__':
    # code below is used to trigger event manually

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file_functional_id',help='File identifier')
    parser.add_argument('-n','--name',required=True,help='Event name')
    parser.add_argument('-m','--model',help='Model name')
    parser.add_argument('-p','--project',default='CMIP5',help='Project name')
    parser.add_argument('-P','--dataset_pattern',help='Dataset pattern')
    args = parser.parse_args()

    if args.name == 'latest_dataset_complete_output12':

        assert args.project is not None
        assert args.model is not None
        assert args.dataset_pattern is not None

        latest_output12_dataset_complete_event(args.project,args.model,args.dataset_pattern,commit=True)
    elif args.name == 'file_complete_event':

        assert args.file_functional_id is not None

        f=sddao.get_file(file_functional_id=args.file_functional_id)

        file_complete_event(f)
    else:
        print_stderr('Incorrect event name')
