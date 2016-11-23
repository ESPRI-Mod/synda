#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains metadata transformation routines."""

import argparse
import sdapp
import sddb
import sdrebuildquery
import sddatasetdao
import sdfiledao
import sdtimestamp
import sdfields
import sdlog
import sddump
import sdutils
from sdprogress import SDProgressDot,SDProgressBar
from sdexception import SDException

def set_checksum_when_empty(file):
    """
    This method compute missing checksum for all files

    never used yet
    """
    for f in sdrebuildquery.get_files_without_checksum():
        checksum_type=sdconst.CHECKSUM_TYPE_MD5
        cs=sdutils.compute_checksum(f.get_full_local_path(),checksum_type)

        f.checksum=cs
        f.checksum_type=checksum_type

        sdfiledao.update(f)

    """Set variable column when NULL (some rows have variable column NULL for historical reasons, this procedure fix that)."""

def set_variable_when_empty():
    transfers=[]
    rege=re.compile("^(.+)/([^/]+)/([^/]+)/[^/]+$")

    i=0
    transfers=sdrebuildquery.get_transfers__variable_null()
    while len(transfers)>0: # loop while there are still rows with variable not set

        # extract variable name from local_path
        for t in transfers: # loop over block of 1000 (optimisation not to load 300000 File objects in memory..)
            rege_result=rege.match(t.getLocalPath()) # sample => MOHC/HadGEM2-ES/piControl/day/atmos/day/r1i1p1/v20110202/sfcWind/sfcWind_day_HadGEM2-ES_piControl_r1i1p1_19091201-19191130.nc
            if rege_result!=None:
                t.variable=rege_result.group(3) # sample => sfcWind
            else:
                raise SDException("SDREBUIL-010","incorrect format")


        # update
        for t in transfers: # loop over block of 1000 (optimisation not to load 300000 CTransfer objects in memory..)
            sdfiledao.update(t,sddb.conn)
            i+=1

        sddb.conn.commit()


        transfers=sdrebuildquery.get_transfers__variable_null()

        SDProgressDot.print_char("|")

    print ""
    print "%i record updated"%i 

def PROC0011():
    """Fix B0032 (set non_normalized_model_name)."""
    sdrebuildquery.update_model_names()

def set_model_when_empty():
    """Fix B0025 bug."""
    datasets=sddatasetdao.get_datasets()

    for d in datasets:
        m=re.search('^[^/]*/([^/]*)/.*$',d.name) # sample => MOHC/HadGEM2-ES/rcp26/day/atmos/day/r1i1p1/v20110524
        if m!=None:
            model=m.group(1)
            d.model(model)
            sdrebuildquery.update_dataset(d)
        else:
            raise SDException("SDREBUIL-120","incorrect dataset format (%s)"%d.getName())
        SDProgressDot.print_char(".")

def set_timestamp_when_empty__BATCH_MODE_1():
    """
    Retrieve *all* datasets from ESGF, then update local timestamp.

    Not used.
    """
    datasets=sddump.dump_ESGF(parameter=['searchapi_host=esgf-data.dkrz.de'],fields=sdfields.get_timestamp_fields())

    sdlog.info("SDREBUIL-008","%i dataset(s) retrieved from ESGF."%len(datasets))
    sdlog.info("SDREBUIL-012","Start updating timestamp in local database.")

    for i,d in enumerate(datasets):

        if 'instance_id' in d: # this is because some dataset have no instance_id in ESGF !
            dataset=sddatasetdao.get_dataset(dataset_functional_id=d['instance_id'])
            if dataset is not None:
                if 'timestamp' in d: # this is because some dataset have no timestamp in ESGF !
                    dataset.timestamp=d['timestamp']
                    sddatasetdao.update_dataset(dataset,commit=False,keys=['timestamp'])

        SDProgressBar.print_progress_bar(len(datasets),i,title="Updating dataset's timestamp.. ")

    SDProgressBar.progress_complete()

    sddb.conn.commit()

def set_timestamp_when_empty__BATCH_MODE_2(project='CMIP5'):
    """
    Retrieve datasets from local database, then retrieve datasets from ESGF, then update local timestamp.
    """
    datasets_without_timestamp=sddatasetdao.get_datasets(project=project,timestamp=None) # retrieve datasets with timestamp not set
    sdlog.info("SDREBUIL-004","Updating %i dataset(s) timestamp."%len(datasets_without_timestamp))
    for dataset_without_timestamp in datasets_without_timestamp:
        try:
            sdtimestamp.fill_missing_dataset_timestamp(dataset_without_timestamp)
        except SDException, e:
            if e.code in ['SDTIMEST-011','SDTIMEST-008','SDTIMEST-800']:
                sdlog.info("SDREBUIL-694","Timestamp not set for dataset (reason=%s,dataset=%s)"%(e.code,dataset_without_timestamp.dataset_functional_id))
            else:
                # fatal error come here

                raise

    sddb.conn.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    set_timestamp_when_empty__BATCH_MODE_2()
