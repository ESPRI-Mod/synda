#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains batch mode SQL queries."""

import sdapp
from sdtypes import File
import sddb
import sddao
import sdconst
import sdsqlutils

# method 1

def get_files_batch(conn=sddb.conn):
    """This method is used to loop over all files (note that we use yield here not to load all the rows in memory !!!)

    Notes:
     -
        this method is like get_files_pagination, but use yield instead of using pagination
     -
        it seems not be possible to do write anywhere in the db file between two yields !!!!
            -
                (SELECT ... FOR UPDATE OF ... is not supported. This is understandable
                considering the mechanics of SQLite in that row locking is redundant as
                the entire database is locked when updating any bit of it)
             -
                if using same connection in select and insert, we get 'OperationalError: cannot commit transaction - SQL statements in progress'
                if using different connection, we get 'OperationalError: database is locked'
    """
    arraysize=100
    c = conn.cursor()

    q="select * from file order by file_id ASC"
    c.execute(q)

    for rs in large_query_helper(c,arraysize):
        yield sdsqlutils.get_object_from_resultset(rs,File)

    c.close()

def large_query_helper(cursor,arraysize):
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

# method 2

def get_files_pagination__reset():
    global pagination_limit,pagination_offset

    pagination_limit=pagination_block_size
    pagination_offset=0

def get_files_pagination(conn=sddb.conn):
    """
    this method is used to loop over all files (note that we use pagination here not to load all the rows in memory)

    notes
      - this method is like get_files_batch(), but use pagination instead of using yield
      - with this method, it is possible to update record along the way
    """
    global pagination_offset

    files=[]
    c = conn.cursor()

    q="select * from file order by file_id ASC limit %d offset %d" % (pagination_limit,pagination_offset)

    # debug
    #print q

    c.execute(q)

    results = c.fetchall()

    for rs in results:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))

    c.close()

    # move OFFSET for the next call
    pagination_offset+=pagination_block_size

    return files

# method 3

def get_files(limit=None,conn=sddb.conn):
    """
    Note
      - if 'limit' is None, retrieve all records
    """
    files=[]

    orderby="file_functional_id"
    limit_clause="limit %i"%limit if limit is not None else ""

    c = conn.cursor()
    q="select * from file order by %s desc %s"%(orderby,limit_clause)
    c.execute(q)
    rs=c.fetchone()
    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))
        rs=c.fetchone()
    c.close()

    return files

# module init.

pagination_offset=0
pagination_limit=0
pagination_block_size=2500
