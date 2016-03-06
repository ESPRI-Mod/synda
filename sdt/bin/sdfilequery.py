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

import humanize
import argparse
import sdapp
import sddb
import sdconst

def transfer_running_count(conn=sddb.conn):
    c=conn.cursor()
    c.execute("select count(1) from file where status = '%s'" % sdconst.TRANSFER_STATUS_RUNNING)
    rs=c.fetchone()

    if rs==None:
        raise SDException("SDSTAQUE-002","fatal error")

    count=rs[0]
    c.close()
    return count

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

def metric():

    if rate
        metric_calculation='cast (avg(rate) as int)'
    elif size
        metric_calculation='cast (sum(size) as int)'
    else:
        assert False

    group_column= # data_node | project | model
    
    where_clause="status='done' and rate is not NULL and size is not NULL"
    if group_column=='model':
        where_clause+=" and project='CMIP5'"

    q='select %s, %s from file where %s group by %s;'%(group_column,metric_calculation,where_clause,group_column)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
