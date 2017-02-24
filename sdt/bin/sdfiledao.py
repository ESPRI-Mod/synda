#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains file DAO SQL queries."""

import sdapp
from sdexception import SDException
import sddb
import sdconfig
import sdsqlutils
from sdtypes import File

def update_transfer_last_access_date(i__date,i__transfer_id,conn=sddb.conn):
    # no commit here (will be committed in updatelastaccessdate())
    c = conn.cursor()
    c.execute("update file set last_access_date=? where file_id = ?",(i__date,i__transfer_id))
    c.close()

def add_file(file,commit=True,conn=sddb.conn):
    keys_to_insert=['status', 'crea_date', 'url', 'local_path', 'filename', 'file_functional_id', 'tracking_id', 'priority', 'checksum', 'checksum_type', 'size', 'variable', 'project', 'model', 'data_node', 'dataset_id', 'insertion_group_id', 'timestamp']
    return sdsqlutils.insert(file,keys_to_insert,commit,conn)

def delete_file(tr,commit=True,conn=sddb.conn):
    c = conn.cursor()

    c.execute("delete from selection__file where file_id=?",(tr.file_id,)) # also delete entries from junction table
    c.execute("delete from file where file_id=?",(tr.file_id,))
    # note that we don't delete entries (if any) from post_processing tables (this will be done in a batch procedure which will be manually executed from time to time)

    # TAGKRE45343J54K5JK
    if c.rowcount<>1:
        raise SDException("SYNCDDAO-908","file not found (file_id=%i,local_path=%s)"%(tr.file_id,tr.local_path,))

    c.close()

    if commit:
        conn.commit()

def exists_file(f,conn=sddb.conn):
    """
    Not used.
    """
    return exists_file_status(f,None,conn)

def exists_files_status(f,i__status,conn=sddb.conn):
    """
    Not used.
    """
    found=False

    c = conn.cursor()

    if i__status!=None:
        q="select 1 from file where local_path='%s' and status='%s'" %(f.local_path,f.project,i__status)
    else:
        q="select 1 from file where local_path='%s'" %(f.local_path,f.project)

    c.execute(q)

    rs=c.fetchone()

    if rs==None:
        found=False
    else:
        found=True

    c.close()

    return found

def get_file(file_functional_id,conn=sddb.conn):
    """
    notes
      - returns None if file not found
      - return type is File
    """
    t=None

    c = conn.cursor()
    c.execute("select * from file where file_functional_id = ?", (file_functional_id,))
    rs=c.fetchone()
    if rs<>None:
        t=sdsqlutils.get_object_from_resultset(rs,File)
    c.close()

    return t

def get_files(limit=None,conn=sddb.conn,**search_constraints): # don't change arguments order here
    """
    Notes
      - one search constraint must be given at least
      - if 'limit' is None, retrieve all records matching the search constraints
    """
    files=[]

    search_placeholder=sdsqlutils.build_search_placeholder(search_constraints)
    orderby="priority DESC, checksum"
    limit_clause="limit %i"%limit if limit is not None else ""

    c = conn.cursor()
    q="select * from file where %s order by %s %s"%(search_placeholder,orderby,limit_clause)
    c.execute(q,search_constraints)
    rs=c.fetchone()
    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))
        rs=c.fetchone()
    c.close()

    return files

def get_dataset_files(d,conn=sddb.conn,limit=None):
    """
    Retrieves all dataset's files

    Args
        limit: if set, returns only a subset of datasets's files
    """
    files=[]

    c = conn.cursor()

    limit_clause="limit %i"%limit if limit is not None else ""

    q="select * from file where dataset_id = %i order by variable %s" % (d.dataset_id,limit_clause)

    c.execute(q)

    rs=c.fetchone()
    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))
        rs=c.fetchone()

    c.close()

    return files

def update_file(file,commit=True,conn=sddb.conn):
    keys=['status','error_msg','sdget_status','sdget_error_msg','start_date','end_date','duration','rate']

    # 'url' need to be present when 'sdnexturl' feature is enabled
    if sdconfig.next_url_on_error:
        keys.append('url')

    rowcount=sdsqlutils.update(file,keys,commit,conn)

    # check
    if rowcount==0:
        raise SDException("SYNCDDAO-121","file not found (file_id=%i)"%(i__tr.file_id,))
    elif rowcount>1:
        raise SDException("SYNCDDAO-120","duplicate functional primary key (file_id=%i)"%(i__tr.file_id,))

