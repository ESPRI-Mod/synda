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
from sdtools import print_stderr
import sdconst

def transfer_running_count(conn=sddb.conn):
    return transfer_status_count(status=sdconst.TRANSFER_STATUS_RUNNING,conn=conn)

def transfer_status_count(status=None,conn=sddb.conn):

    assert status!=None

    c=conn.cursor()
    q="select count(1) from file where status = '%s'" % status
    c.execute(q)
    rs=c.fetchone()

    if rs==None:
        raise SDException("SDSTAQUE-002","fatal error")

    count=rs[0]
    c.close()
    return count

def get_download_status(project=None):
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

def get_metrics(group_,metric,project_,dry_run=False):
    li=[]

    c = sddb.conn.cursor()



    # check

    assert group_ in ['data_node','project','model']
    assert metric in ('rate','size')

    # WARNING: we don't check project_ for sql injection here. This MUST be done in the calling func. TODO: check for sql injection here



    # prepare metric calculation

    if metric=='rate':
        metric_calculation='avg(rate)'
    elif metric=='size':
        metric_calculation='sum(size)'



    # prepare where clause

    where_clause="status='done' and rate is not NULL and size is not NULL"

    if group_=='model':
        where_clause+=" and project='%s'"%project_



    # execute

    q='select %s, %s as metric from file where %s group by %s order by metric desc'%(group_,metric_calculation,where_clause,group_)



    if dry_run:
        print_stderr('%s'%q)   
        return []


    c.execute(q)

    rs=c.fetchone()
    while rs!=None:
        group_column_value=rs[0]
        metric_column_value=rs[1]

        li.append((group_column_value,metric_column_value))

        rs=c.fetchone()


    c.close()

    return li

def get_download_speed_over_time():
    li=[]

    q="""
      select
        datetime(
                cast(   
                        (   
                            strftime('%s', start_date) /* cast date to timestamp */
                            / (24*60*60) /* time mark every 24 hours */
                        )
                as int ) /* round (i.e. remove decimal. This is where is the core intelligence of this query) */
            * (24*60*60), /* revert (without the decimal part, of course) */
        'unixepoch') interval, /* revert */
        avg(rate) rate_by_day
      from file
      where status in ('done')
      group by interval order by interval
      """

    return li

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    li=get_download_status()
    print li
