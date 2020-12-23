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

_HISTORY_COLUMNS="action,crea_date,selection_filename,insertion_group_id,selection_file_checksum"

def add_history_line(action,selection_filename=None,insertion_group_id=None,crea_date=None,selection_file_checksum=None,conn=sddb.conn):

    crea_date=sdtime.now() if crea_date is None else crea_date

    c = conn.cursor()
    c.execute("insert into history (action, selection_filename, crea_date, insertion_group_id, selection_file_checksum) values (?,?,?,?,?)",(action, selection_filename, crea_date, insertion_group_id,selection_file_checksum))
    c.close()
    conn.commit()

def get_all_history_lines(conn=sddb.conn):
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

def get_history_lines(selection_filename,action,conn=sddb.conn):
    li=[]
    c = conn.cursor()

    query="select %s from history where selection_filename = ? and action = ?"%_HISTORY_COLUMNS
    c.execute(query,(selection_filename,action))

    rs=c.fetchone()
    while rs!=None:
        li.append(sdsqlutils.resultset_to_dict(rs))
        rs=c.fetchone()
    c.close()

    return li

def get_latest_history_line(selection_filename,action,conn=sddb.conn):
    c = conn.cursor()

    query="select %s from history where selection_filename = ? and action = ? order by crea_date DESC LIMIT 1"%_HISTORY_COLUMNS
    c.execute(query,(selection_filename,action))
    rs=c.fetchone()

    assert rs is not None # existency test must be done before calling this func

    di=sdsqlutils.resultset_to_dict(rs)
    c.close()

    return di

# module init.
