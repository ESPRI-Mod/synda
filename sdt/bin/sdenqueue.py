#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script inserts rows in "transfer" and "dataset" tables.

Notes
    - This filter terminates a pipeline
    - This module is intended to be plugged to sdfilepipeline output
      (i.e. stream must be duplicate free and each file must contain status attribute).
"""

import sys
import argparse
import json
import sdapp
import sdlog
import sddb
import sdsimplefilter
import sdhistory
import sdfiledao
import sddatasetdao
import sdutils
import sdconfig
import sdtimestamp
from sdtypes import Dataset,File
import sdconst
import sdsqlutils
import sdpostpipelineutils
import sdtime
import sdpipelineprocessing
from sdexception import SDException
import sdprogress

def run(metadata,timestamp_right_boundary=None):
    """
    Returns
        Number of enqueued items.
    """

    if metadata.count() < 1:
        return 0

    f=metadata.get_one_file()
    selection_filename=sdpostpipelineutils.get_attached_parameter__global([f],'selection_filename') # note that if no files are found at all for this selection (no matter the status), then the filename will be blank
    selection_file=sdpostpipelineutils.get_attached_parameter__global([f],'selection_file') # note that if no files are found at all for this selection (no matter the status), then 'selection_file' will be blank
    

    metadata=sdsimplefilter.run(metadata,'status',sdconst.TRANSFER_STATUS_NEW,'keep')

    count=metadata.count() # how many files to be inserted
    total_size=metadata.size

    if count>0:

        sdlog.info("SDENQUEU-102","Add insertion_group_id..")

        insertion_group_id=sdsqlutils.nextval('insertion_group_id','history') # this is uniq identifier for all inserted files during this run
        po=sdpipelineprocessing.ProcessingObject(add_insertion_group_id,insertion_group_id)
        metadata=sdpipelineprocessing.run_pipeline(metadata,po)

        if sdconfig.progress:
            sdprogress.ProgressThread.start(sleep=0.1,running_message='',end_message='') # spinner start

        sdlog.info("SDENQUEU-103","Insert files and datasets..")

        po=sdpipelineprocessing.ProcessingObject(add_files)
        metadata=sdpipelineprocessing.run_pipeline(metadata,po)

        sdlog.info("SDENQUEU-104","Fill timestamp..")

        fix_timestamp()

        sddb.conn.commit() # final commit (we do all insertion/update in one transaction).

        if sdconfig.progress:
            sdprogress.ProgressThread.stop() # spinner stop

        histo_crea_date=sdtime.search_api_datetime_format_to_sqlite_datetime_format(timestamp_right_boundary) if timestamp_right_boundary is not None else None

        sdhistory.add_history_line(action=sdconst.ACTION_ADD,selection_file=selection_file,insertion_group_id=insertion_group_id,crea_date=histo_crea_date)

    sdlog.info("SDENQUEU-001","%i new file(s) added (total size=%i,selection=%s)"%(count,total_size,selection_filename))

    return count

def add_insertion_group_id(files,insertion_group_id):
    for f in files:
        f['insertion_group_id']=insertion_group_id
    return files

def keep_recent_datasets(datasets):
    """This func is a hack."""
    li=[]

    # Note that we use last_mod_date instead of crea_date, so to also
    # try to retrieve timestamp for previously inserted dataset
    # (i.e. dataset which have been modified during this discovery
    # (i.e. new files have been added to the dataset), but which have
    # been created in a previous discovery).
    #
    # We only try to retrieve timestamp for recent datasets (-24H).
    # This is to prevent retrieving timestamp for datasets not related
    # to the current discovery, because for example, there are 20 000
    # datasets without timestamp on VESG4, and we don't want to trigger
    # 20 000 search-API request each time we install a new file !


    for d in datasets:
    
        interval=sdtime.compute_time_delta(d.last_mod_date,sdtime.now())
        if interval > ( 24 * 3600 ):
            # This dataset has not been modified in the last 24 hours, 
            # so it is not related to the current discovery.

            pass
        else:
            li.append(d)

    return li

def add_files(files):
    for f in files:
        add_file(File(**f))
    return [] # nothing to return (end of processing)

def add_file(f):
    sdlog.info("SDENQUEU-003","Create transfer (local_path=%s,url=%s)"%(f.get_full_local_path(),f.url))

    f.dataset_id=add_dataset(f)
    f.status=sdconst.TRANSFER_STATUS_WAITING
    f.crea_date=sdtime.now()

    sdfiledao.add_file(f,commit=False)

def add_dataset(f):
    """
    Returns:
        dataset_id
    """
    d=sddatasetdao.get_dataset(dataset_functional_id=f.dataset_functional_id)
    if d is not None:

        # check dataset local path format
        #
        # (once a dataset has been created using one local_path format, it
        # cannot be changed anymore without removing the all dataset /
        # restarting the dataset from scratch).
        #
        if d.local_path!=f.dataset_local_path:
            raise SDException("SDENQUEU-008","Incorrect local path format (existing_format=%s,new_format=%s)"%(d.local_path,f.dataset_local_path))

        # compute new dataset status
        if d.status==sdconst.DATASET_STATUS_IN_PROGRESS:
            d.status=sdconst.DATASET_STATUS_IN_PROGRESS

        elif d.status==sdconst.DATASET_STATUS_EMPTY:
            d.status=sdconst.DATASET_STATUS_EMPTY

        elif d.status==sdconst.DATASET_STATUS_COMPLETE:
            d.status=sdconst.DATASET_STATUS_IN_PROGRESS # this means that a dataset may be "in-progress" and also "latest"


        # Note related to the "latest" dataset column
        #
        # Adding new files to a datasets may change the status, but don't
        # change dataset "latest" flag.  This is because a dataset can only
        # downgrade here ("complete" => "in-progress"), or stay the same. And
        # when a dataset downgrade, "latest" flag, if true, stay as is, and if
        # false, stay as is also.

        # "last_mod_date" is only modified here (i.e. it is not modified when
        # dataset's files status change). in other words, it changes only when
        # adding new files to it using this script.
        #
        d.last_mod_date=sdtime.now()


        sddatasetdao.update_dataset(d,commit=False)

        return d.dataset_id

    else:
        sdlog.info("SDENQUEU-002","create dataset (dataset_path=%s)"%(f.dataset_path))

        d=Dataset()

        d.local_path=f.dataset_local_path
        d.path=f.dataset_path
        d.path_without_version=f.dataset_path_without_version
        d.dataset_functional_id=f.dataset_functional_id
        d.template=f.dataset_template
        d.version=f.dataset_version
        d.project=f.project
        d.status=sdconst.DATASET_STATUS_EMPTY
        d.latest=False
        d.crea_date=sdtime.now()
        d.last_mod_date=sdtime.now()

        # non-mandatory attributes
        d.timestamp=f.dataset_timestamp if hasattr(f,'dataset_timestamp') else None
        d.model=f.model if hasattr(f,'model') else None

        return sddatasetdao.add_dataset(d,commit=False)

def fix_timestamp():

    # HACK 1
    #
    # Once all insertions are done, we update 'dataset.timestamp' column (this
    # cannot be done in one step, because dataset 'timestamp' attribute doesn't
    # exist in file's attributes).
    #
    # 'timestamp' is mainly (only ?) needed by sddatasetversion.compare() func
    #
    # Indeed, this code is a hack that makes the workflow less readable
    # (i.e. 'search' then 'enqueue' then 'search' again). Maybe try to improve
    # this in the future. Still, it not as bad as if 'search' triggers 'search'
    # recursively, because in our case, when the second search starts, the
    # first search is completed (AFAIR sdsearch is protected not to permit
    # recursion anyway). 
    # But if needed, there is a way to trigger search recursively: use
    # sdquicksearch (also in this case, sdsearch can still be used for the top
    # level search (so resulting with a mix of sdsearch and sdquicksearch)).
    #
    datasets_without_timestamp=sddatasetdao.get_datasets(timestamp=None) # retrieve datasets with timestamp not set

    # HACK 2
    recent_datasets_without_timestamp=keep_recent_datasets(datasets_without_timestamp)

    if len(recent_datasets_without_timestamp)>0:
        sdlog.info("SDENQUEU-004","Retrieving timestamp for %i dataset(s)."%len(recent_datasets_without_timestamp))

        for dataset_without_timestamp in recent_datasets_without_timestamp:

            try:
                sdtimestamp.fill_missing_dataset_timestamp(dataset_without_timestamp)
            except SDException, e:
                if e.code in ['SDTIMEST-011','SDTIMEST-008','SDTIMEST-800']:
                    sdlog.info("SDENQUEU-909","Timestamp not set for '%s' dataset (%s)"%(dataset_without_timestamp.dataset_functional_id,str(e)))
                else:
                    # fatal error come here

                    raise

    else:
        # This case is when new files are enqueued, but only on existing
        # dataset (so there is no dataset timestamp to update).

        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--priority',required=False,type=int,default=None)
    args = parser.parse_args()

    files=json.load( sys.stdin )

    if args.priority is not None:

        # overide default priority
        for f in files:
            f['priority']=args.priority

    run(files)
