#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains event DAO SQL queries."""

import argparse
import spapp
import spsqlutils
import spconst
import spdb
from sptypes import Event
from spexception import SPException

def add_events(events):
    keys_to_insert=['name', 'status', 'project', 'model', 'dataset_pattern', 'variable', 'filename_pattern', 'crea_date', 'priority']

    conn=spdb.connect()

    try:
        for event in events:
            spsqlutils.insert(event,keys_to_insert,conn)
        conn.commit()
    finally:
        spdb.disconnect(conn)

def get_events(limit=None,**search_constraints):
    """
    Note
      - one search constraint must be given at least
      - if 'limit' is None, retrieve all records
    """
    events=[]

    search_placeholder=spsqlutils.build_search_placeholder(search_constraints)
    orderby="priority DESC, crea_date ASC" # as currently all event have same priority, oldest event always come first
    limit_clause="limit %i"%limit if limit is not None else ""

    conn=spdb.connect()

    c = conn.cursor()
    q="select * from event where %s order by %s %s"%(search_placeholder,orderby,limit_clause)
    c.execute(q,search_constraints)
    rs=c.fetchone()
    while rs!=None:
        events.append(spsqlutils.get_object_from_resultset(rs,Event))
        rs=c.fetchone()
    c.close()

    spdb.disconnect(conn)

    return events

def update_events(events,conn):
    keys=['status'] # TODO: maybe add this too => ,'last_mod_date'

    for e in events:
        rowcount=spsqlutils.update(e,keys,conn)
    
        # check
        if rowcount==0:
            raise SPException("SPEVEDAO-001","event not found (event_id=%s)"%e.event_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    for e in get_events(limit=10,status=spconst.EVENT_STATUS_NEW):
        print str(e)
