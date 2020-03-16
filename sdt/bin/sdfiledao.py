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
import sdlog
from sdtime import SDTimer
import sdconst
import sdsqlitedict

def update_transfer_last_access_date(i__date,i__transfer_id,conn=sddb.conn):
    # no commit here (will be committed in updatelastaccessdate())
    c = conn.cursor()
    c.execute("update file set last_access_date=? where file_id = ?",(i__date,i__transfer_id))
    c.close()

def add_file(file,commit=True,conn=sddb.conn):
    keys_to_insert=['status', 'crea_date', 'url', 'local_path', 'filename', 'file_functional_id', 'tracking_id', 'priority', 'checksum', 'checksum_type', 'size', 'variable', 'project', 'model', 'data_node', 'dataset_id', 'insertion_group_id', 'timestamp', 'searchapi_host']

    if not sdconst.GET_FILES_CACHING:
        return sdsqlutils.insert(file,keys_to_insert,commit,conn)
    else:
        id_ = sdsqlutils.insert(file,keys_to_insert,commit,conn)

        priority = file.__dict__['priority']
        data_node = file.__dict__['data_node']
        hipri = highest_waiting_priority( data_node )
        if hipri is None or priority>hipri:
            # Compute cached max(priority) for the data node, ignoring any previous value.
            highest_waiting_priority( data_node, True )

        return id_

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
    gfs0 = SDTimer.get_time()

    data_node = search_constraints.get('data_node',None)

    # Is the cache applicable to this situation?  Then use it, unless it's empty.
    if set(search_constraints.keys())==set(['status','data_node']) and\
       search_constraints['status']==sdconst.TRANSFER_STATUS_WAITING and\
       limit==1 and\
       sdconst.GET_FILES_CACHING:
        # ...limit==1 isn't essential, but the present coding is for limit==1
        use_cache = True
        if len( get_files.files.get( data_node, [] ) )>0:
            gfs1 = SDTimer.get_elapsed_time( gfs0, show_microseconds=True )
            sdlog.info("SDFILDAO-200","get_files time is %s, used cache, data_node %s"%\
                       (gfs1,data_node))
            return [ get_files.files[data_node].pop(0) ]
        else:
            cachelen = 100
            limit += cachelen
    else:
        use_cache = False

    files=[]
    c = conn.cursor()

    search_placeholder=sdsqlutils.build_search_placeholder(search_constraints)
    limit_clause="limit %i"%limit if limit is not None else ""

    getfirst = priority_clause( data_node, use_cache, c )
    if getfirst=='':
        return []
    q="select * from file where %s %s %s"%(search_placeholder,getfirst,limit_clause)
    c.execute(q,search_constraints)
    rs=c.fetchone()

    #if use_cache and (rs is None or len(rs)==0):
    if use_cache and (rs is None or len(rs)==0):
        # No files found.  Possibly we could find one if we retry at another priority level.
        # Note that it makes no sense to do this if getfirst==''.  That has alread triggered
        # an early return.
        highest_waiting_priority( data_node, c )   # compute the priority to retry at
        getfirst = priority_clause( data_node, use_cache, c )
        q="select * from file where %s %s %s"%(search_placeholder,getfirst,limit_clause)
        c.execute(q,search_constraints)
        rs = c.fetchone()

    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))
        rs=c.fetchone()
    c.close()

    if len(files)>1 and use_cache:
        # We shall return one of the files and cache the rest.
        get_files.files[ data_node ] = files[1:]
        files = files[0:1]

    gfs1 = SDTimer.get_elapsed_time( gfs0, show_microseconds=True )
    sdlog.info("SDFILDAO-200","get_files time is %s, search %s with %s"%(gfs1,q,search_constraints))
    return files
get_files.files = {}

def priority_clause( data_node, use_cache, cursor ):
    if use_cache:
        pri = highest_waiting_priority(data_node)
        if pri is None:
            getfirst = ''
        else:
            getfirst = "AND priority=%s" % pri
    else:
        getfirst = "ORDER BY priority DESC, checksum"
    return getfirst

def highest_waiting_priority( data_node, cursor=None, connection=sddb.conn ):
    """This function contains a dictionary-like cache of the highest priority among status='waiting'
    files for each data_node.  It will always return the dictionary value for the specified
    data node, or one of the specified data nodes if several are provided.
    - When called with a data_node and cursor, it will update its value for that data_node.
    - If cursor==True, then this function will create and close its own cursor.
    - If data_node==True, then this function will be applied to all data nodes.
    """
    if cursor is None:
        return (highest_waiting_priority.vals).get(data_node,None)
    else:
        if cursor==True:
            c = connection.cursor()
        else:
            c = cursor
        if data_node==True:
            q = "SELECT data_node FROM file GROUP BY data_node"
            c.execute(q)
            data_nodes = [tup[0] for tup in c.fetchall()]
        else:
            data_nodes = [data_node]
        for dn in data_nodes:
            hwp0 = SDTimer.get_time()
            q = "SELECT MAX(priority) FROM file WHERE status='waiting' AND data_node='%s'" % dn
            c.execute(q)
            val = c.fetchone()
            if len(val)>0:
                highest_waiting_priority.vals[dn] = val[0]
            else:
                highest_waiting_priority.vals.pop(dn,None)
            hwp1 = SDTimer.get_elapsed_time( hwp0, show_microseconds=True )
            #sdlog.info("SDFILDAO-300","time %s to recompute priority=%s for %s" %
            #           (hwp1,val[0],dn) )
            #sdlog.info("SDFILDAO-301","  query %s" % q )
        if cursor==True:
            c.close()
        return (highest_waiting_priority.vals).get(data_nodes[0],None)
# The cache is a database masquerading as a dictionary.  A real dictionary in memory would be:
# highest_waiting_priority.vals = {}
highest_waiting_priority.vals=sdsqlitedict.SqliteStringDict(
    sdconfig.default_db_folder+"/caches.db", 'maxpri', None )

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
    keys=['status','error_msg','sdget_status','sdget_error_msg','start_date','end_date','duration','rate','priority']

    # 'url' needs to be present when 'sdnexturl' feature is enabled
    if sdconfig.next_url_on_error:
        keys.append('url')
        keys.append('searchapi_host')

    rowcount=sdsqlutils.update(file,keys,commit,conn)

    # check
    if rowcount==0:
        raise SDException("SYNCDDAO-121","file not found (file_id=%i)"%(i__tr.file_id,))
    elif rowcount>1:
        raise SDException("SYNCDDAO-120","duplicate functional primary key (file_id=%i)"%(i__tr.file_id,))

