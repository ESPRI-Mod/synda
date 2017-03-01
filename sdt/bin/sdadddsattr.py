#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module add datasets attributes to files.

This module has been developed, because some users need to use datasets level
attribute when using local path custom mode ('local_path_drs_template'). 

TAG543J53K45JK34

Notes
    - 'sdadddsattr' means "SynDa ADD DataSet ATTRibutes"
    - this module retrieves datasets attributes in batch mode.
TODO
    - merge this module with 'sdbatchtimestamp' module to prevent download datasets twice (TBC)
    - only retrieve fields used in 'local_path_drs_template' (TAGJ43JK55J8K78 and TAG3JKWW93K4J4JKDZS)
"""

import argparse
import sdapp
import sdrun
import copy
import sdlog
import sdpipelineprocessing
from sdexception import MissingDatasetUrlException

def run(squeries,metadata,parallel):
    datasets_attrs=None

    try:
        datasets_attrs=get_datasets_attrs(squeries,parallel)
    except MissingDatasetUrlException,e:
        sdlog.error("SDADDDSA-108","Datasets cannot be set as dataset url is missing")
        return metadata

    sdlog.info("SDADDDSA-100","%d datasets retrieved"%len(datasets_attrs))

    sdlog.info("SDADDDSA-306","Copy dataset attrs..")
    po=sdpipelineprocessing.ProcessingObject(add_dataset_attrs,datasets_attrs)
    metadata=sdpipelineprocessing.run_pipeline(metadata,po)

    return metadata

def get_datasets_attrs(squeries,parallel):

    # switch url
    for q in squeries:
        q['url_tmp']=q['url']

        if 'dataset_attrs_url' not in q:
            sdlog.info("SDADDDSA-300","dataset_attrs_url not found in query")
            raise MissingDatasetUrlException()

        q['url']=q['dataset_attrs_url']


    sdlog.info("SDADDDSA-301","Submit dataset queries..")

    # run
    ds_metadata=sdrun.run(squeries,parallel)

    sdlog.info("SDADDDSA-304","Transform data struct..")

    # transform to dict for quick random access
    di={}
    for d in ds_metadata.get_files(): # warning: load list in memory
        instance_id=d['instance_id']
        di[instance_id]=d

    # restore url
    for q in squeries:
        q['url']=q['url_tmp']
        del q['url_tmp']

    return di

def add_dataset_attrs(files,datasets_attrs):
    datasets_not_found=set()

    for f in files:
        dataset_functional_id=f['dataset_functional_id']

        if dataset_functional_id in datasets_attrs:

            # TAGJ43JK55J8K78
            for k,v in datasets_attrs[dataset_functional_id].iteritems():
                if k not in f:
                    f[k]=copy.deepcopy(v)
                else:
                    pass # do not overwrite if already existing

        else:
            datasets_not_found.add(dataset_functional_id)

    for dataset_functional_id in datasets_not_found:
        sdlog.info("SDADDDSA-200","dataset not found (%s)"%dataset_functional_id)

    return files

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
