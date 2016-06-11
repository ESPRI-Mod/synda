#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains history dao."""

import sdapp
import sddb
import sdsqlutils
import sdtime

_HISTORY_COLUMNS="action,crea_date,selection_filename,insertion_group_id"

def add_history_line(action,selection_filename=None,insertion_group_id=None,conn=sddb.conn):
    c = conn.cursor()
    c.execute("insert into history (action, selection_filename, crea_date, insertion_group_id) values (?,?,?,?)",(action, selection_filename, sdtime.now(), insertion_group_id))
    c.close()
    conn.commit()

def get_history_lines(conn=sddb.conn):
    li=[]
    c = conn.cursor()
    query="select %s from history"%_HISTORY_COLUMNS
    c.execute(query)
    rs=c.fetchone()
    while rs!=None:
        li.append(sdsqlutils.resultset_to_dict(rs))
        rs=c.fetchone()
    c.close()
    return li

def get_latest_history_line():
    pass # FIXME

# module init.
