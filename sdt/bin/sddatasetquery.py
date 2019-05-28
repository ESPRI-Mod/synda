#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains dataset special queries (i.e. non-dao)

Also see
    sddatasetdao.py
"""

import argparse
import sdapp
import sddb
import sdconst
import sdsqlutils
from sdtypes import Dataset
from sddatasetversion import DatasetVersions

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
