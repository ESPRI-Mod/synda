#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

import argparse
import sdapp
import sddeletefile
import sdlog
import sddao
import sdfiledao
import sddatasetdao
import sdconst
import sdmodifyquery
import sddatasetflag

def delete_insertion_group(insertion_group_id):
    files=sdfiledao.get_files(insertion_group_id=insertion_group_id)
    files=[f for f in files] # exclude files already marked for deletion
    if len(files)>0:
        for f in files:
            sddeletefile.deferred_delete(f.file_functional_id)
            sdlog.info("SYDADMIN-001","File marked for deletion (%s)"%f.file_functional_id)
        print "%i file(s) marked for deletion"%len(files)
        sddao.add_history_line(sdconst.ACTION_DELETE,insertion_group_id=insertion_group_id)
    else:
        print "Nothing to delete"

def cleanup2():
    """
    not used for now

    1. error and waiting cleaning
    2. recalculate dataset flags (latest & status).This step is
       important, otherwise, some datasets version may switch to 'latest' as the
       dataset now looks like 'complete (based on the fact that all the remaining
       files are 'done').
    """
    global_cleanup()

    # discovery process is needed here (./start.sh -a) to prevent switching
    # some datasets to latest while there are in fact not complete (we see them
    # as complete just because error & waiting have been removed..).

    set_datasets_flags()

def set_datasets_flags():
    """Set dataset status and latest flag."""
    count=0

    sdlog.info("SDOPERAT-933","recalculate status and latest flag for all dataset..",True)

    sdmodifyquery.reset_datasets_flags() # we reset all flags before starting the main processing (we clean everything to start from scratch)

    count=update_datasets__status_and_latest()
    while count>0:
        count=update_datasets__status_and_latest()

def update_datasets__status_and_latest():
    """
    set status and latest flag for all datasets

    return value
     returns how many datasets have been modified

    note
        - this procedure must be run until no modifications remain (a run makes changes, which impact the next one, and so one. after a few runs, the graph traversal must be complete)
    """
    datasets_modified_count=0

    i=0
    for d in sddatasetdao.get_datasets():

        # store dataset current state
        l__latest=d.latest
        l__status=d.status

        # compute new 'status' flag
        d.status=sddatasetflag.compute_dataset_status(d)
        sddatasetdao.update_dataset(d)

        # compute new 'latest' flag
        if not d.latest: # we check here the current value for 'latest' flag
            sddatasetflag.update_latest_flag(d) # warning: this method modifies the dataset in memory (and in database too)
        else:
            # nothing to do concerning the 'latest' flag as the current dataset is already the latest
            # (the latest flag can only be switched off (i.e. to False) by *other* datasets versions, not by himself !!!)
            pass

        # check if the dataset has changed
        if l__latest!=d.latest or l__status!=d.status:
            datasets_modified_count+=1

        # display progress
        if i%2==0:
            SDProgressDot.print_char(".")

        i+=1

    print ""
    sdlog("SDOPERAT-630","modified datasets: %i"%datasets_modified_count)

    return datasets_modified_count

def set_latest_flag(path):
    """This method is used to manually set the 'latest' flag."""

    d=sddatasetdao.get_dataset(path=path,raise_exception_if_not_found=False) # retrieve dataset from database
    if d is not None:
        if d.latest==True:
            print "'latest' flag is already set for this dataset"
        else:
            sddatasetflag.update_latest_flag(d,force_latest=True) # warning: this method modifies the dataset in memory (and in database too)
    else:
        print "Dataset not found"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action',choices=['delete'],required=True)
    parser.add_argument('-i', '--insertion_group_id')
    args = parser.parse_args()

    if args.insertion_group_id is not None:
        delete_insertion_group(args.insertion_group_id)
