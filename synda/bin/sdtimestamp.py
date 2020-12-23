#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains timestamp related func."""

import argparse
import sdapp
import sdconst
import sddatasetdao
import sdquicksearch
import sdlog
import sdprint
from sdexception import SDException

def fill_missing_dataset_timestamp(dataset_without_timestamp):
    """This funcs set the dataset timestamp.

    Notes
        - This func DO NOT commit.
        - In ESFG, timestamp differs from replica to replica, and so, as there
          is no dataset replica concept in 'sdt', it's really a hack, because
          we set the timestamp randomly (i.e. dataset's timestamp in
          Synda installation at user A may differ to dataset's timestamp
          in Synda installation at user B (because the timestamp for the
          dataset may have been retrieved from replica X in the case of user A
          and from replica Y in the case of user B (and X replica's timestamp
          may differ from Y replica's timestamp))). Anyway, in the end, we
          hope that the timestamp random is on a much smaller scale than the
          version-to-version time interval scale, so to be able to detect which
          version is the latest ! And yes: all this mess is because version exists
          in different formats ('v1', 'v20140318'..).
    """

    # Retrieve timestamps from ESGF
    # Note
    #     We do not filter replica in the query below in case the master host is not up
    result=sdquicksearch.run(parameter=['limit=1','fields=%s'%timestamp_fields,'type=Dataset','instance_id=%s'%dataset_without_timestamp.dataset_functional_id],post_pipeline_mode=None)
    li=result.get_files()

    # check if dataset has been found in ESGF
    if len(li)>0:
        d=li[0]
    else:
        raise SDException("SDTIMEST-800","%s dataset does not exist in ESGF (or the index used does not list it)"%dataset_without_timestamp.dataset_functional_id)

    # use file's timestamp if dataset's timestamp is not set in ESGF
    # (this is needed, because some dataset in ESGF have NO timestamp...)
    use_file_timestamp_if_dataset_timestamp_is_missing(d)

    # update timestamp in DB
    dataset=sddatasetdao.get_dataset(dataset_functional_id=d['instance_id'])
    dataset.timestamp=d['timestamp']
    sddatasetdao.update_dataset(dataset,commit=False,keys=['timestamp'])

def use_file_timestamp_if_dataset_timestamp_is_missing(d):

    if 'timestamp' not in d:
        # timestamp doesn't exist in ESGF for this dataset

        # hack
        #
        # Use a dataset's (random (i.e. files have not always the same even
        # timestmap in one dataset, so we take one randomly)) file timestamp
        # as dataset's timestamp is missing in ESGF !

        # Note
        #     We do not filter replica in the query below in case the master host is not up
        result=sdquicksearch.run(parameter=['limit=1','fields=%s'%timestamp_fields,'type=File','dataset_id=%s'%d['instance_id']],post_pipeline_mode=None)
        li=result.get_files()
        if len(li)>0:
            file=li[0]

            if 'timestamp' in file:

                d['timestamp']=file['timestamp']

                sdlog.info("SDTIMEST-001","Dataset timestamp set from one dataset's file's timestamp (dataset_functional_id=%s,file_functional_id=%s)"%(d['instance_id'],file['instance_id']))
            else:
                raise SDException("SDTIMEST-008","Timestamp missing in both dataset and dataset's file(s) (%s)"%d['instance_id'])
        else:
            raise SDException("SDTIMEST-011","Dataset exist in ESGF, but is empty (%s)"%d['instance_id'])

# init.

timestamp_fields=','.join(sdconst.TIMESTAMP_FIELDS)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('parameter',nargs='*',default=[])
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()
