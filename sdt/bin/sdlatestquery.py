#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains sql queries related to 'latest' flag."""

import sdapp
import sddb
from sdtypes import Dataset

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
