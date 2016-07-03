#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing pipeline run DAO SQL queries.

Note
    - 'spppprdao' means 'Synchro-Data Post-Processing Pipeline Run Data Access Object'
"""

import spapp
import spdb
import spsqlutils
import spconst
from sptypes import PPPRun
from spexception import SPException,NoPostProcessingTaskWaitingException
import splog

def exists_ppprun(pppr,conn):
    c=conn.cursor()
    #splog.debug("SPPPPRDA-101","%s,%s,%s"%(pppr.pipeline,pppr.dataset_pattern,pppr.variable))
    c.execute("select 1 from ppprun where pipeline=? and dataset_pattern=? and variable=? ",(pppr.pipeline,pppr.dataset_pattern,pppr.variable))
    rs=c.fetchone()
    found=False if (rs==None) else True
    c.close()
    return found

def add_ppprun(pppr,conn): # 'pppr' means 'Post-Processing Pipeline Run'
    keys_to_insert=['project', 'model', 'state', 'transition', 'status', 'crea_date', 'priority', 'variable', 'dataset_pattern', 'pipeline']
    spsqlutils.insert(pppr,keys_to_insert,conn)

def get_pppruns(order=None,conn=None,limit=None,**search_constraints): # don't change arguments order here
    """
    Notes
      - one search constraint must be given at least
      - if 'limit' is None, retrieve all records
    """
    ppps=[] # 'ppps' means 'Post-Processing PipelineS'

    # remove None values (i.e. sql NULL is not supported in this method)
    search_constraints=dict((k, search_constraints[k]) for k in search_constraints if search_constraints[k] is not None)

    if order=='aspgf': # 'aspgf' means 'Already Started Pipelines Go First'
        # in this case, we try to complete one pipeline as soon as possible
        orderby="priority DESC, last_mod_date DESC"
    elif order=='fifo':
        # in this case, we process job class in FIFO order
        orderby="priority DESC, crea_date ASC"
    else:
        raise SPException("SPPPPRDA-006","incorrect value for 'order' (%s)"%order)

    search_placeholder=spsqlutils.build_search_placeholder(search_constraints) # note that placeholders is only used for scalar value
    multivalues_filters=spsqlutils.build_multivalues_filters(search_constraints)

    where_clause_items=[search_placeholder,multivalues_filters]

    where_clause=' AND '.join(filter(lambda x: len(x)>0,where_clause_items))
    limit_clause="limit %i"%limit if limit is not None else ""

    c = conn.cursor()
    q="select * from ppprun where %s order by %s %s"%(where_clause,orderby,limit_clause)
    #splog.debug("SPPPPRDA-100","%s"%q)
    c.execute(q,search_constraints)
    rs=c.fetchone()
    while rs!=None:
        ppps.append(spsqlutils.get_object_from_resultset(rs,PPPRun))
        rs=c.fetchone()
    c.close()

    return ppps

def get_ppprun(ppprun_id):
    """
    Note
        returns None if ppprun not found
    """
    ppprun=None

    conn=spdb.connect()

    c=conn.cursor()
    c.execute("select * from ppprun where ppprun_id = ?", (ppprun_id,))
    rs=c.fetchone()
    if rs<>None:
        ppprun=spsqlutils.get_object_from_resultset(rs,PPPRun)
    c.close()

    spdb.disconnect(conn)

    return ppprun

def get_one_waiting_ppprun(job_class,pipeline,order,conn):
    li=get_pppruns(limit=1,status=spconst.PPPRUN_STATUS_WAITING,transition=job_class,pipeline=pipeline,conn=conn,order=order)

    if len(li)==0:
        raise NoPostProcessingTaskWaitingException()
    else:
        pppr=li[0]

    return pppr

def update_ppprun(ppprun,conn): # 'ppprun' means 'Post-Processing Pipeline run'
    keys=['transition','state','status','error_msg','last_mod_date']

    rowcount=spsqlutils.update(ppprun,keys,conn)

    # check
    if rowcount==0:
        raise SPException("SPPPPRDA-001","Post-processing pipeline run not found (ppprun_id=%i)"%(ppprun.ppprun_id,))
    elif rowcount>1:
        raise SPException("SPPPPRDA-002","Duplicate primary key (ppprun_id=%i)"%(ppprun.ppprun_id,))
