#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains statistics SQL queries"""

import humanize
import argparse
import sdapp
import sddb
import sdconst
import sdsqlutils
from sdtypes import DatasetVersions,Dataset
import sddao

def get_selection_stats(us,status):
    size=0
    count=0
    c = sddb.conn.cursor()

    c.execute("select size, count(1) from selection__transfer ust,file t where ust.transfer_id=t.transfer_id and t.status=? and ust.selection_id=?",(status,us.getSelectionID(),))

    #self.log("SDSTAT-INF110",""%(,))

    rs=c.fetchone()
    size=rs[0] if (rs[0] is not None) else 0 # this is because count(1) return 0 when not found, but sum(stuff) returns None
    count=rs[1]
    c.close()

    return (size,count)

def get_selections_stats(status):
    size=0
    count=0
    c = sddb.conn.cursor()
    c.execute("select size, count(1) from file where status=?",(status,))
    rs=c.fetchone()
    size=rs[0] if (rs[0] is not None) else 0 # this is because count(1) return 0 when not found, but sum(stuff) returns None
    count=rs[1]
    c.close()

    return (size,count)

def get_dataset_stats(d):
    stat={}
    stat['size']={}
    stat['count']={}

    # init everything to zero
    for status in sdconst.TRANSFER_STATUSES_ALL:
        stat['size'][status]=0
        stat['count'][status]=0
        stat['variable_count']=0

    c = sddb.conn.cursor()

    # -- size by status -- #
    c.execute("select status,sum(size) as size from file where dataset_id=? group by status",(d.dataset_id,))
    rs=c.fetchone()
    while rs is not None:
        stat['size'][rs['status']]=rs['size']
        rs=c.fetchone()

    # -- count by status -- #
    c.execute("select status,count(1) as count from file where dataset_id=? group by status",(d.dataset_id,))
    rs=c.fetchone()
    while rs is not None:
        stat['count'][rs['status']]=rs['count']
        rs=c.fetchone()

    # -- how many variable, regardless of the file status -- #
    c.execute("select count(distinct variable) from file where dataset_id=?",(d.dataset_id,))
    rs=c.fetchone()
    count=rs[0]
    stat['variable_count']=count

    c.close()
    return stat

def get_download_status(project):
    li=[]

    c = sddb.conn.cursor()

    if project is None:
        q="select status,count(*),sum(size) from file group by status"
        c.execute(q)
    else:
        q="select status,count(*),sum(size) from file where project=? group by status"
        c.execute(q,(project,))

    rs=c.fetchone()
    while rs!=None:
        status=rs[0]
        count=rs[1]
        size=humanize.naturalsize(rs[2],gnu=False)

        li.append([status,count,size])

        rs=c.fetchone()

    c.close()

    return li

def transfer_running_count(conn=sddb.conn):
    c=conn.cursor()
    c.execute("select count(1) from file where status = '%s'" % sdconst.TRANSFER_STATUS_RUNNING)
    rs=c.fetchone()

    if rs==None:
        raise SDException("SDSTAQUE-002","fatal error")

    count=rs[0]
    c.close()
    return count

def count_dataset_files(d,file_status,conn=sddb.conn):
    c = conn.cursor()

    if file_status is None:
        c.execute("select count(1) from file where dataset_id=?",(d.dataset_id,))
    else:
        c.execute("select count(1) from file where dataset_id=? and status=?",(d.dataset_id,file_status,))

    rs=c.fetchone()
    nbr=rs[0]

    c.close()
    return nbr

def get_dataset_versions(i__d,i__compute_stats):
    datasetVersions=DatasetVersions()

    c = sddb.conn.cursor()
    c.execute("select * from dataset where path_without_version=?",(i__d.path_without_version,))
    rs=c.fetchone()
    while rs!=None:

        l__d=sdsqlutils.get_object_from_resultset(rs,Dataset)
        if i__compute_stats:
            l__d.statistics=get_dataset_stats(l__d)
        datasetVersions.add_dataset_version(l__d)

        rs=c.fetchone()
    c.close()

    return datasetVersions

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
