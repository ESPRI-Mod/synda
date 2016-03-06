#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains local dataset flags refresh routines."""

import sdapp
import sddb
import sddao
import sddatasetdao
import sdfilequery
import sddatasetquery
import sdconst
import sddatasetutils
import sdutils
import sdtime
import sdlog
import sdvariable
import sdmodifyquery
from sdprogress import SDProgressDot
from sdexception import SDException

def switch_off_latest_flag_for_all_other_versions(latest_dataset_version,dataset_versions):
    """
    Notes
      - This method is called manually and by the daemon
    """
    if dataset_versions.count()>1: # if other versions of this dataset exist

        # note that we change other datasets here only if the transfer dataset change too
        # (at least for the latest flag, which switch from false to true)
        # so if you call this method and the dataset stays the same, 
        # you are sure that nothing was changed in the database by this method

        # switch all other versions to False (set "latest" flag of all other versions of this dataset to false)
        for l__d in dataset_versions.get_datasets():

            if l__d.version<>latest_dataset_version: # exclude ourself. As we are now the latest, we don't want to be set to False here, of course..

                l__d.latest=False
                sddatasetdao.update_dataset(l__d,False,sddb.conn)

def update_latest_flag(d,force_latest=False):
    """
    Args:
        force_latest: If 'true', force 'latest' to 'true' no matter what the compute_latest_flag() method say)

    Notes
     - warning: this method update the dataset in database (and in some cases, also all other different versions of this datasets)
     - warning: this method modifies 'd' object
    """

    assert not d.latest # this func must NOT be called if the dataset is already 'latest'

    dataset_versions=sddatasetquery.get_dataset_versions(d,True) # retrieves all dataset versions

    d.latest=True if force_latest else compute_latest_flag(dataset_versions,d) # set the *new* value for the 'latest' flag

    if d.latest==True:
        # if we are here, it means latest switch from False to True

        d.latest_date=sdtime.now() # "latest_date" is set when dataset "latest" flag switches from False to True
        switch_off_latest_flag_for_all_other_versions(d.version,dataset_versions) # MOD_A
    else:
        # the latest stay false, do nothing

        pass

    sddatasetdao.update_dataset(d,False,sddb.conn) # MOD_B
    sddb.conn.commit() # commit all datasets modifications together (MOD_A (if any) and MOD_B)

def compute_latest_flag(dataset_versions,d):
    """
    Note
        when this func is called, d.latest is false
    """
    l__latest=None

    assert d.status is not None

    if dataset_versions.count()==0:
        # assert

        raise SDException("SYDDFLAG-206","fatal error") # should never occurs

    elif dataset_versions.count()==1:
        # this is the first version

        if d.status==sdconst.DATASET_STATUS_EMPTY:
            # do not contains any complete variable yet

            l__latest=False

        elif d.status==sdconst.DATASET_STATUS_IN_PROGRESS:
            # In this case, we set the current dataset to false as only complete dataset can be latest (new behaviour from 2014-09-17)

            l__latest=False
        elif d.status==sdconst.DATASET_STATUS_COMPLETE:
            # this case is very less likely to occurs,
            # because the intermediary step (in-progress) should have 
            # already switched the latest flag to true (and we don't come here
            # if latest is already set to true).
            # one reason maybe when there is only one variable in the dataset

            l__latest=True
        else:
            raise SDException("SYDDFLAG-106","fatal error") # should never occurs

    elif dataset_versions.count()>1:
        # there are others versions

        if d.status==sdconst.DATASET_STATUS_EMPTY:
            # do not contains any complete variable yet

            l__latest=False

        elif d.status==sdconst.DATASET_STATUS_IN_PROGRESS:

            if not dataset_versions.exists_version_with_latest_flag_set_to_true():
                # many dataset versions without anyone having the latest flag set

                # in multi-version modes, many dataset versions can be in "in-progress" state without the anyone having the latest flag set to True yet.
                # In this case, we set the current dataset to false as only complete dataset can be latest (new behaviour from 2014-09-17)
                
                l__latest=False
            else:

                # important note: a dataset can downgrade from "complete" to "in-progress"
                #                 (if we add some new variables, etc..)
                #                 and in this case, if the "latest" flag was already true, we don't want it to downgrade to false !!!
                #                 but this shouldn't happen, because a dataset can only be "latest downgraded" by *another* dataset,
                #                 which must be complete and have higher version number. and this is the normal case.

                if dataset_versions.is_most_recent_version_number(d):
                    # the dataset is in-progress and have the latest version number

                    # we wait until it is complete

                    l__latest=False
                else:
                    # we wait until it is complete
                    # but anyway, even when it will complete, it is less likely that it will pass "latest", because there is a version ahead
                    # but it still may occurs in rare occasion

                    l__latest=False

        elif d.status==sdconst.DATASET_STATUS_COMPLETE:

            if dataset_versions.is_most_recent_version_number(d): # WARNING: isMostRecentVersionNumber() is not related with latest flag !!
                # the dataset just completed and have the latest version *NUMBER* (not the latest flag, the number !!)

                if not dataset_versions.exists_version_with_latest_flag_set_to_true():
                    # we set latest if no other have the latest flag

                    l__latest=True
                else:

                    if qualitycheck_ok(dataset_versions,d):

                        l__latest=True
                    else:
                        # it is not possible to automatically determine if this version can be set to 'latest'
                        # so we don't promote to 'latest' but we inform the administrator for manual intervention
                        #
                        sdlog.info("SYDDFLAG-739","'latest' flag not set for '%s'. you can set it manually with './start.sh -L %s'"%(d.get_full_local_path(),d.dataset_functional_id))
                        
                        l__latest=False
            else:
                # this case may occurs in multi-version mode
                # (two versions can be downloaded simultaneously)
                
                if not dataset_versions.exists_version_with_latest_flag_set_to_true():
                    # we set latest if no other have the latest flag

                    l__latest=True
                else:
                    if dataset_versions.is_version_higher_than_latest(d):
                        # we also set latest flag to true if the current latest flag is on an older version

                        if qualitycheck_ok(dataset_versions,d):

                            l__latest=True
                        else:
                            # it is not possible to automatically determine if this version can be set to 'latest'
                            # so we don't promote to 'latest' but we inform the administrator for manual intervention
                            #
                            #
                            # WARNING
                            #  note that this log is only useful in multi-version mode !
                            #  (in last-version mode, those version will not grow anymore, so you can ignore them)
                            #
                            sdlog.info("SYDDFLAG-740","'latest' flag not set for '%s'. you can set it manually with './start.sh -L %s'"%(d.get_full_local_path(),d.dataset_functional_id))
                            
                            l__latest=False

                    else:
                        # we set to False here, as we never downgrade a "latest"
                         
                        l__latest=False

        else:
            raise SDException("SYDDFLAG-064","fatal error") # should never occurs
    
    return l__latest

def compute_dataset_status(d):
    """This method compute the dataset transfer status."""
    l__status=None

    # retrieve global infos
    #
    total_files_count=sdfilequery.count_dataset_files(d,None)
    total_done_files_count=sdfilequery.count_dataset_files(d,sdconst.TRANSFER_STATUS_DONE)


    #########################
    #     status flag
    #########################
    if total_done_files_count==0:
        l__status=sdconst.DATASET_STATUS_EMPTY
    else:
        # TODO
        # some special status should not be considered done: sdconst.TRANSFER_STATUS_DELETE

        if total_files_count == total_done_files_count:
            l__status=sdconst.DATASET_STATUS_COMPLETE
        else:

            if sdvariable.exists_one_complete_variable(d):
                # for a dataset to be set "in-progress", it must contains at least one complete variable

                # note that it is possible to downgrade a dataset from
                # "in-progress" to "empty" by adding some new files (i.e. you
                # can exclude time slices from the variable).  so you can add
                # new time slices to an already downloaded variable which will
                # then need to be switched to empty.
                # 
                # TODO => how/where is it switched to empty ?

                l__status=sdconst.DATASET_STATUS_IN_PROGRESS
            else:
                l__status=sdconst.DATASET_STATUS_EMPTY

    return l__status

def qualitycheck_ok(dataset_versions,d):
    """
    based on some statistics, this method accepts or deny 'latest' promotion for the dataset 'd'

    return
        false if 'd' don't seem ready to be promoted to 'latest'
        true  if 'd' seems ready to be promoted to 'latest'
    """

    # retrieve stats for current latest flagged version
    latest_dataset=dataset_versions.get_dataset_with_latest_flag_set()
    current_version_stats=latest_dataset.statistics

    # retrieve stats for candidate version for 'latest' promotion
    candidate_stats=sddatasetquery.get_dataset_stats(d)

    # assert
    if latest_dataset.dataset_id==d.dataset_id:
        raise SDException("SYDDFLAG-140","fatal error (%i)"%d.dataset_id)

    # variable number quality check
    if candidate_stats['variable_count'] < (current_version_stats['variable_count'] * 0.5) : # if variable number drops
        sdlog.info("SYDDFLAG-730","%s"%d.get_full_local_path())
        return False

    # total file number quality check
    """
    if candidate_stats.getFilesCount() < current_version_stats.getFilesCount(): # if file number decrease
        sdlog.info("SYDDFLAG-734","%s"%d.get_full_local_path())
        return False
    """

    return True

def reset_datasets_flags():
    """Reset dataset status and latest flag from scratch for all datasets."""
    count=0

    sdlog.info("SYDDFLAG-933","recalculate status and latest flag for all dataset..",True)

    sdmodifyquery.wipeout_datasets_flags() # we reset all flags before starting the main processing (we clean everything to start from scratch)

    count=update_datasets__status_and_latest()
    while count>0:
        count=update_datasets__status_and_latest()

def update_datasets__status_and_latest():
    """
    Set status and latest flag for all datasets.

    Return value
        Returns how many datasets have been modified

    Note
        This procedure must be run until no modifications remain (a run makes
        changes, which impact the next one, and so one. after a few runs, the
        graph traversal must be complete)
    """
    datasets_modified_count=0

    i=0
    for d in sddatasetdao.get_datasets():

        # store dataset current state
        l__latest=d.latest
        l__status=d.status

        # compute new 'status' flag
        d.status=compute_dataset_status(d)
        sddatasetdao.update_dataset(d)

        # compute new 'latest' flag
        if not d.latest: # we check here the current value for 'latest' flag
            update_latest_flag(d) # warning: this method modifies the dataset in memory (and in database too)
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
    sdlog.info("SYDDFLAG-630","modified datasets: %i"%datasets_modified_count)

    return datasets_modified_count
