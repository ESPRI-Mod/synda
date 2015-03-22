#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdevent.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script contains event related routines."""

import sdvariable
import sddatasetdao
import sddatasetflag
import sdproduct
import sdeventdao
import sdconst
import sdtime
import sdlog
from sdtypes import Event

""" TODO: add deletion pipeline
def file_deleted_event(d):
    sdlog.debug("SYDEVENT-030","'delete_dataset_event' triggered")

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
    sdlog.debug("SYDEVENT-001","'file_complete_event' triggered")

    # update dataset (all except 'latest' flag)
    tr.dataset.status=sddatasetflag.compute_dataset_status(tr.dataset)
    tr.dataset.last_done_transfer_date=tr.end_date
    sddatasetdao.update_dataset(tr.dataset)

    if sdvariable.is_variable_complete(tr.dataset.dataset_id,tr.variable):
        variable_complete_event(tr.project,tr.model,tr.dataset,tr.variable) # trigger 'variable complete' event

def variable_complete_event(project,model,dataset,variable):
    sdlog.debug("SYDEVENT-002","'variable_complete_event' triggered")

    # cascade 1
    if dataset.status==sdconst.DATASET_STATUS_COMPLETE:
        dataset_complete_event(project,model,dataset) # trigger 'dataset complete' event

    # cascade 2
    if project=='CMIP5':

        assert '/output/' not in dataset.path

        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset.path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if sdvariable.is_variable_complete(d1.dataset_id,variable) and sdvariable.is_variable_complete(d2.dataset_id,variable):
                dataset_pattern=sdproduct.build_output12_dataset_pattern(dataset.local_path)
                variable_complete_output12_event(project,model,dataset_pattern,variable) # trigger event (cross dataset event)
        else:
            # we also trigger the 'variable_complete_output12_event' event if the variable is over one product only (because if only one product, then output12 event is also true)

            dataset_pattern=sdproduct.build_output12_dataset_pattern(dataset.local_path)
            variable_complete_output12_event(project,model,dataset_pattern,variable) # trigger event (cross dataset event)

def variable_complete_output12_event(project,model,dataset_pattern,variable,commit=True):
    sdlog.debug("SYDEVENT-003","'variable_complete_output12_event' triggered")

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
    sdlog.debug("SYDEVENT-004","'dataset_complete_event' triggered")

    if project=='CMIP5':
        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset.path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if d1.status==sdconst.DATASET_STATUS_COMPLETE and d2.status==sdconst.DATASET_STATUS_COMPLETE:
                dataset_pattern=sdproduct.build_output12_dataset_pattern(dataset.local_path)
                dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)

                if d1.latest and d2.latest:
                    latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)
                elif not d1.latest and not d2.latest:
                    non_latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)
                else:
                    sdlog.warning("SYDEVENT-032","Event not triggered as one product is latest while the other product is not") # TODO: is this the right way to handle this case ?
        else:
            dataset_pattern=sdproduct.build_output12_dataset_pattern(dataset.local_path)
            dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)

            if dataset.latest:
                latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)
            else:
                non_latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=commit)

    # <<<--- 'latest' flag management related code begin

    # store current 'latest' flag state
    old_latest=dataset.latest

    # compute new 'latest' flag
    if not old_latest:
        # old state is not latest

        sddatasetflag.update_latest_flag(dataset) # warning: this method modifies the dataset in memory (and in database too)
    else:
        # nothing to do concerning the 'latest' flag as the current dataset is already the latest
        # (the latest flag can only be switched off (i.e. to False) by *other* datasets versions, not by himself !!!)
        pass

    # store new 'latest' flag state
    new_latest=dataset.latest

    # --->>> 'latest' flag management related code end


    # cascade 2
    if (not old_latest) and new_latest:
        dataset_latest_event(project,model,dataset.path,commit=commit) # trigger 'dataset_latest' event

def dataset_complete_output12_event(project,model,dataset_pattern,commit=True):

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

def latest_dataset_complete_output12_event(project,model,dataset_pattern,commit=True):
    # this event means one latest dataset has been completed (i.e. was latest before and still is)

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

    # cascade
    if project=='CMIP5':
        assert '/output/' not in dataset_path

        (ds_path_output1,ds_path_output2)=sdproduct.get_output12_dataset_paths(dataset_path)
        if sddatasetdao.exists_dataset(path=ds_path_output1) and sddatasetdao.exists_dataset(path=ds_path_output2):

            d1=sddatasetdao.get_dataset(path=ds_path_output1)
            d2=sddatasetdao.get_dataset(path=ds_path_output2)

            if d1.latest and d2.latest:
                dataset_pattern=sdproduct.build_output12_dataset_pattern(dataset_path)
                dataset_latest_output12_event(project,model,dataset_pattern,commit=commit) # trigger event
        else:
            dataset_pattern=sdproduct.build_output12_dataset_pattern(dataset_path)
            dataset_latest_output12_event(project,model,dataset_pattern,commit=commit) # trigger event

def dataset_latest_output12_event(project,model,dataset_pattern,commit=True):

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
