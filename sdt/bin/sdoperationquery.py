#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdoperationquery.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains sql queries used by operational routines."""

import sdapp
import sddb
import sddao
import sddatasetdao
import sdlargequery
from sdtypes import Dataset
from sdprogress import SDProgressDot

def get_latest_datasets(full,conn=sddb.conn):
    """Returns datasets with latest flag set to true."""
    datasets=[]

    if full:
        q="select * from dataset where latest=1 and project in ('GeoMIP','CMIP5') order by project"
    else:
        q="select * from dataset where latest=1 and project in ('GeoMIP','CMIP5') and latest_date > date('now','-10 days') order by project"

    c = conn.cursor()
    c.execute(q)
    rs=c.fetchone()
    while rs!=None:
        datasets.append(sdsqlutils.get_object_from_resultset(rs,Dataset))
        rs=c.fetchone()
    c.close()

    return datasets

def get_latest_datasets_to_export(project,conn=sddb.conn):
    """
    returns datasets with latest flag set to true

    2014-09-24: BEWARE, this func is obsolete and not used anymore.
                This operation is now handled by the SDPP module, 
                using 'dataset complete' event as trigger for publishing.
                Note that number of variables in the dataset and number of files
                in the dataset must be attached to the event so to prevent 
                publication overflood (i.e. to keep same mecanisms as in this
                routine).

    note
      used by crontab procedure
    """
    datasets=[]

    c = conn.cursor()


    # process batch only (second member of the main query)
    #
    # notes
    #   - this is a PATCH to process all the datasets at least once as fast as we can (the daily incremental part has been removed)
    #   - the daily incremental part slow down the batch part, because it may process again and again the same datasets every night
    #     as long as new files are downloaded..
    #   - comments have been removed (see the main query for comments)
    #
    #q="""
    #select * from dataset 
    #where latest=1 and dataset_id not in (select distinct dataset_id from export)
    #  and project=%s
    #order by last_done_transfer_date desc
    #"""%(project,)


    # process incremental and batch (main query)
    #
    # note
    #  - it may be useful to always keep the batch part of the query, as
    #    this is a security if too much datasets are downloaded at the same
    #    time, or if the export crontab procedure stops during a few days
    #    (this member will be empty most of the time anyway, 
    #    (i.e. we will not send datasets through the pipeline which do
    #    not need to be processed by the pipeline))
    #
    #
    q="""
      /* this union member is for incremental processing: it will contain rows as long as already exported dataset have new modifications */
      /* strange column alias below are normal: this is not to confuse sqlite (latest_export__dataset_id) */
      select dataset.* from 
        (select dataset_id as latest_export__dataset_id,max(export_date) as last_export_date from export group by dataset_id) latest_export,                  /* retrieves datasets last export date */
        dataset
      where 
        dataset.latest=1 and dataset.dataset_id=latest_export.latest_export__dataset_id                                                                             /* main join clause (only returns datasets which exist in export table, i.e. which have already been exported */
        and project='%s'
        and dataset.last_done_transfer_date > latest_export.last_export_date                                                                                        /* only keep datasets with fresh modifications */
    union
      /* this union member is for batch processing: it will contain rows as long as never exported datasets exist (with latest flag set to true, of course..). */
      select * from dataset 
      where latest=1 and dataset_id not in (select distinct dataset_id from export)                                                                           /* this retrieve dataset which have never been exported yet */
        and project='%s'
    order by last_done_transfer_date desc                                                                                                                           /* "order by" here is global to both union members. "desc" is to process recently modified first */
    """%(project,project)

    c.execute(q)

    rs=c.fetchone()
    while rs!=None:
        datasets.append(sdsqlutils.get_object_from_resultset(rs,Dataset))
        rs=c.fetchone()

    c.close()

    return datasets

def populate_selection_transfer_junction():
    """
    populate "selection__transfer" association table

    WARNING: this method is only CMIP5 DRS compatible
    """
    sdlargequery.get_files_pagination__reset()

    transfer_without_selection=0
    transfer_without_dataset=0
    i=0
    transfers=sdlargequery.get_files_pagination() # loop over block (trick not to load 300000 CTransfer objects in memory..). Size is given by pagination_block_size
    while len(transfers)>0:
        for t in transfers:
            d=sddatasetdao.get_dataset(dataset_id=t.dataset_id)
            if d is not None:
                t.setDataset(d)
            else:
                insert_transfer_without_dataset(t)
                transfer_without_dataset+=1

                # we can't go on without dataset (contains() method needs it)
                continue

            # selection<=>transfer mapping and insertion in assoc table
            orphan=1 # this is to detect orphan transfer (i.e. don't belong to any selection)
            for us in get_Selections():

                # debug
                #print "%s<=>%s"%(t.getTransferID(),us.getSelectionID())

                if us.contains(t):

                    sddao.insert_selection_transfer_junction(t,us,_conn) # no commit inside
                    orphan=0

            if orphan==1:
                inserttransferwithoutselection(t)
                transfer_without_selection+=1


        _conn.commit() # commit block of insertSelectionTransferJunction

        # display progress
        #if i%100==0:
        SDProgressDot.print_char(".")

        i+=1



        transfers=sdlargequery.get_files_pagination()


    if transfer_without_selection>0:
        sdlog.log("SDMIGR-ERR032","%d transfer(s) not matching any selection found"%transfer_without_selection)

    if transfer_without_dataset>0:
        sdlog.log("SDMIGR-ERR033","%d missing dataset transfer(s) found"%transfer_without_dataset)
