#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains batch mode SQL queries.

Also see
    sddbpagination
"""

import sdapp
from sdtypes import File
import sddb
import sdsqlutils

# method 1

def get_files_batch(conn=sddb.conn):
    """This method is used to loop over all files (note that we use yield here not to load all the rows in memory !)

    Notes:
     - this method is like get_files_pagination, but use yield instead of using pagination
     - it seems not be possible to do write anywhere in the db file between two yields !!!!
         -
            (SELECT ... FOR UPDATE OF ... is not supported. This is understandable
            considering the mechanics of SQLite in that row locking is redundant as
            the entire database is locked when updating any bit of it)
         -
            - if using same connection in select and insert, we get 'OperationalError: cannot commit transaction - SQL statements in progress'
            - if using different connection, we get 'OperationalError: database is locked'
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
