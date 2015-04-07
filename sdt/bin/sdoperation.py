#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains operation routines."""

import os
import commands
import argparse
import sdapp
import sddatasetflag
from sdprogress import SDProgressDot
import sdconfig
import sdlog
import sdoperationquery
import sdstatquery
import sdutils
import sddao
import sddeletedataset
import sdvariable
import sddb
import sdproduct
import sdevent
from sdexception import SDException

def print_recently_modified_datasets():
    """Export to prodiguer.

    Note
      to be used on PRODIGFS only and with CMIP5 like DRS only (i.e. we need DRS with the product (not the case for obs4mips, for example..))
    """
    datasets=get_recently_modified_datasets()

    for d in datasets:
        sddao.store_dataset_export_event(d) # insert entry in export table
        print "%s/latest"%d.get_full_local_path_without_version()

def get_recently_modified_datasets():
    files_count=0
    dataset_count=0
    max_total_files_count=30000 # do not export more than this everyday (change it from 30000 to 10000 if a second stream for IPSL data is added)
    max_files_count_per_dataset=1000000 # this is not to export dataset with too much files (if we don't do that, the server crashes). It has a huge value, as this problem seems now to be obsolete
    datasets_to_export=[]

    for d in sdoperationquery.get_latest_datasets_to_export("CMIP5"): # currently, we only export CMIP5 project to prodiguer

        # retrieve how many files in the dataset
        dataset_stats=sdstatquery.get_dataset_stats(d) 

        if dataset_stats['count']['done'] > max_files_count_per_dataset:
            # dataset contains too much files, do not process it

            sdlog.info("SDOPERAT-424","dataset not exported as it contains too much files (local_path=%s,files_count=%i)"%(d.get_full_local_path(),dataset_stats['count']['done'],))
            continue

        if (files_count+dataset_stats['count']['done'])<max_total_files_count: # is there still free room to process this dataset
            # there is free room

            files_count+=dataset_stats['count']['done']

            datasets_to_export.append(d)

            sdlog.info("SDOPERAT-322","export %s"%d.get_full_local_path())
        else:
            # we reached the files count limit
            break

    dataset_count=len(datasets_to_export)
    sdlog.info("SDOPERAT-324","datasets exported: %i"%dataset_count)
    sdlog.info("SDOPERAT-325","total files exported: %i"%files_count)

    return datasets_to_export

def trigger_events():
    """Artificially trigger event (usually, events are triggered after each transfer completion).

    This func is used, for example, to trigger pipeline on already downloaded data.
    """

    li=sdvariable.get_complete_variables(project='CMIP5')

    # add the dataset_pattern (used in the next step to remove duplicates)
    for v in li:
        v.dataset_pattern=sdproduct.build_output12_dataset_pattern(v.dataset_path)

    # Remove duplicates
    #
    # Duplicate exist because of those two facts:
    #   - we have '*' in product in dataset pattern
    #   - there are cases when a variable exist on both product (output1 and output2)
    #
    di={}
    for v in li:
        di[(v.dataset_pattern,v.name)]=v

    # load
    for v in di.values():
        SDProgressDot.print_char(".")
        sdevent.variable_complete_output12_event(v.project,v.model,v.dataset_pattern,v.name,commit=False)
    sddb.conn.commit() # we do all insertion commit in one transaction

def cleanup_tree():
    """Remove empty files and folders."""
    sdlog.info("SDOPERAT-008","Starting cleanup in %s."%sdconfig.data_folder)

    # TODO: this method is only used for incremental mode and it would be usefull to be able to also have a full mode cleanup

    argv=[sdconfig.cleanup_tree_script,sdconfig.data_folder]

    (status,stdout,stderr)=sdutils.get_status_output(argv)
    if status!=0:
        raise SDException("SDOPERAT-001","Error occurs during tree cleanup (see 'cleanup_tree.log' for details)")

    sdlog.info("SDOPERAT-010","Cleanup done.")

def recreate_selection_transfer_association_table():
    """Reset "selection__transfer" association table (populate from scratch)."""
    truncate_selection_transfer_junction()
    truncate_orphan_tables()
    populate_selection_transfer_junction()

def remove_orphan_files():
    """Remove files not matching any selection (orphan transfers)."""

    # first we check if those files are being used (by checking "last access date" on the filesysem)
    #transfers=getOrphanTransfers()

    pass

def update_last_access_date():
    """Refresh "file.last_access_date" for all transfers."""
    get_files_pagination__reset()

    transfers_without_file=0 # transfers in DB but not in FS
    transfers=get_files_pagination() # loop over block (trick not to load 300000 CTransfer objects in memory..). Size is given by pagination_block_size
    while len(transfers)>0:
        for t in transfers:

            # keep only "done" transfers
            if t.getStatus() != sdconst.TRANSFER_STATUS_DONE:
                continue

            # retrieve "last access date"
            l__date=None
            try:
                l__date=sdutils.get_last_access_date(t)
            except FileNotFoundException,e:
                sdlog.error("SDOPERAT-632","File missing on filesystem (%s)"%t.get_full_local_path())
                transfers_without_file+=1
                continue

            except SDException,e:
                sdlog.error("SDOPERAT-532","Fatal error")
                raise

            # set new date in DB
            updatetransferlastaccessdate(l__date,t.file_id)

        sddb._conn.commit() # commit block of insertSelectionTransferJunction
        SDProgressDot.print_char(".")
        transfers=get_files_pagination()

    if transfers_without_file>0:
        sdlog.error("SDOPERAT-132","%d files missing on filesystem"%transfers_without_file)

def print_latest_datasets_full():
    print_latest_datasets(True)

def print_latest_datasets_recent():
    print_latest_datasets(False)

def print_latest_datasets(full):
    """
    Note
        Used by symlink.sh script
    """
    for d in sdoperationquery.get_latest_datasets(full):
        print d.get_full_local_path()

# init.

procs={
    'PROC0001': sddeletedataset.purge_orphan_datasets,
    'PROC0006': print_recently_modified_datasets,
    'PROC0008': recreate_selection_transfer_association_table,
    'PROC0009': print_latest_datasets_full,
    'PROC0010': print_latest_datasets_recent,
    'PROC0011': trigger_events
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--procedure',required=True)
    args = parser.parse_args()

    procs[args.procedure]()
