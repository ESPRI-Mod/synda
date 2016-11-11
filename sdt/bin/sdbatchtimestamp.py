#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module retrieves timestamp in batch mode."""

import copy
import sdapp
import sdrun
import sdlog
import sdconst
import sdpipelineprocessing
from sdexception import MissingDatasetTimestampUrlException,MissingTimestampException

def run(squeries,metadata,parallel):
    datasets_timestamps=None


    try:
        datasets_timestamps=get_datasets_timestamps(squeries,parallel)
    except MissingDatasetTimestampUrlException,e:
        sdlog.error("SYNDABTI-600","Datasets timestamps cannot be set as dataset_timestamp_url is missing")
        return metadata

    sdlog.info("SYNDABTI-100","%d datasets with timestamp retrieved"%len(datasets_timestamps))

    sdlog.info("SYNDABTI-306","Set missing timestamp..")

    po=sdpipelineprocessing.ProcessingObject(add_dataset_timestamp,datasets_timestamps)
    metadata=sdpipelineprocessing.run_pipeline(metadata,po)

    return metadata

def add_dataset_timestamp(files,datasets_timestamps):
    dataset_with_missing_timestamp=set()

    for f in files:
        dataset_functional_id=f['dataset_functional_id']

        if dataset_functional_id in datasets_timestamps:
            f['dataset_timestamp']=datasets_timestamps[dataset_functional_id]
        else:
            dataset_with_missing_timestamp.add(dataset_functional_id)

    for dataset_functional_id in dataset_with_missing_timestamp:
        sdlog.info("SYNDABTI-200","dataset timestamp not found (%s)"%dataset_functional_id)

    return files

def get_datasets_timestamps(squeries,parallel):

    # switch url
    for q in squeries:
        q['url_tmp']=q['url']

        if 'dataset_timestamp_url' not in q:

            sdlog.info("SYNDABTI-300","dataset_timestamp_url not found in query")

            raise MissingDatasetTimestampUrlException() # just in case (should be always set for 'install' action)

        q['url']=q['dataset_timestamp_url']

    
    sdlog.info("SYNDABTI-301","Submit timestamp queries..")

    # run
    metadata=sdrun.run(squeries,parallel)

    sdlog.info("SYNDABTI-304","Transform timestamp data struct..")

    # transform to dict for quick random access
    di={}
    for d in metadata.get_files(): # warning: load list in memory
        instance_id=d['instance_id']

        try:
            timestamp=get_timestamp(instance_id,d)
            di[instance_id]=timestamp
        except MissingTimestampException, e:
            sdlog.info("SYNDABTI-500","dataset found but dataset timestamp is missing (%s)"%instance_id)

    # restore url
    for q in squeries:
        q['url']=q['url_tmp']
        del q['url_tmp']

    return di

def get_timestamp(instance_id,d):
    if 'timestamp' in d:
        timestamp=d['timestamp']
    elif '_timestamp' in d:
        timestamp=d['_timestamp']
    else:
        raise MissingTimestampException() # just in case (should be always set for 'install' action)

    return timestamp
