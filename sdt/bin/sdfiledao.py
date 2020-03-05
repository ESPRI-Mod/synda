#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved"
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

    id_ = sdsqlutils.insert(file,keys_to_insert,commit,conn)

    priority = file.__dict__['priority']
    hipri = highest_waiting_priority( f['data_node'] )
    if hipri is None or priority>hipri:
        # Compute cached max(priority) for the data node, ignoring any previous value.
        highest_waiting_priority( f['data_node'], True )

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
    gfs0 = SDTimer.get_time() #jfp

    data_node = search_constraints.get('data_node',None)

    # Was this function was called by sddao.get_one_waiting_transfer(), with data_node specified?
    if limit==1 and\
       set(search_constraints.keys())==set(['status','data_node']) and\
       search_constraints['status']==sdconst.TRANSFER_STATUS_WAITING:
        from_gowt = True
        if len( get_files.files.get( data_node, [] ) )>0:
            gfs1 = SDTimer.get_elapsed_time( gfs0, show_microseconds=True ) #jfp
            sdlog.info("JFPFLDAO-200","get_files time is %s, used cache, data_node %s"%\
                       (gfs1,data_node))
            return [ get_files.files[data_node].pop(0) ]
        else:
            cachelen = 100
    else:
        from_gowt = False

    files=[]
    c = conn.cursor()

    #sdlog.info("JFPSDDAO-140","search_constraints=%s"%search_constraints)
    #sdlog.info("JFPSDDAO-141","limit=%s"%limit)
    search_placeholder=sdsqlutils.build_search_placeholder(search_constraints)
    #orderby="priority DESC, checksum"
    if from_gowt:
        sdlog.info("JFPFLDAO-145","limit=%s,type %s cachelen=%s, type %s"%\
                   (limit,type(limit),cachelen,type(cachelen) ))
        limit_clause="limit %i"%(limit+cachelen) if limit is not None else ""
    else:
        limit_clause="limit %i"%limit if limit is not None else ""
    #sdlog.info("JFPSDDAO-146","limit_clause=%s"%limit_clause)
    getfirst = priority_clause( data_node, from_gowt, c )
        
    #sdlog.info("JFPSDDAO-148","getfirst=%s"%getfirst)

    # was q="select * from file where %s order by %s %s"%(search_placeholder,orderby,limit_clause)
    q="select * from file where %s %s %s"%(search_placeholder,getfirst,limit_clause)
    #sdlog.info("JFPSDDAO-150","query=%s"%q)
    c.execute(q,search_constraints)
    rs=c.fetchone()
    if (rs is None or len(rs)==0) and from_gowt:
        # No files found.  Possibly we could find them if we retry at another priority level.
        highest_waiting_priority( data_node, c )
        getfirst = priority_clause( data_node, from_gowt, c )
        q="select * from file where %s %s %s"%(search_placeholder,getfirst,limit_clause)
        c.execute(q,search_constraints)
        rs = c.fetchone()
    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))
        rs=c.fetchone()
    c.close()
    #sdlog.info("JFPFLDAO-152","files=%s"%files)

    if len(files)>1 and from_gowt:
        # We shall return one of the files and cache the rest.
        get_files.files[ data_node ] = files[1:]
        files = files[0:1]

    gfs1 = SDTimer.get_elapsed_time( gfs0, show_microseconds=True ) #jfp
    sdlog.info("JFPFLDAO-200","get_files time is %s, search %s with %s"%(gfs1,q,search_constraints))
    return files
get_files.files = {}

def priority_clause( data_node, from_gowt, cursor ):
    #sdlog.info("JFPFLDAO-260","Entering priority_clause, args=%s,%s,%s,%s"%
    #           ( data_node, from_gowt, cursor ) )
    if from_gowt:
        #sdlog.info("JFPFLDAO-262","will compute pri")
        pri = highest_waiting_priority(data_node)
        #sdlog.info("JFPFLDAO-263","pri=%s"%pri)
        if pri is None:
            pri = highest_waiting_priority(data_node, cursor)
        if pri is None:
            getfirst = ''
        else:
            getfirst = "AND priority=%s" % pri
    else:
        getfirst = "ORDER BY priority DESC, checksum"
    #sdlog.info("JFPFLDAO-270","getfirst=%s"%getfirst)
    return getfirst

def highest_waiting_priority( data_node, cursor=None, connection=sddb.conn ):
    """This function contains a dictionary of the highest priority among status='waiting' files for
    each data_node.  It will always return the dictionary value for the specified data node, or
    one of the specified data nodes if several are provided.
    - When called with a data_node and cursor, it will update its value for that data_node.
    - If cursor==True, then this function will create and close its own cursor.
    - If data_node==True, then this function will be applied to all data nodes.
    (deprecated If cursor is a string with the special value "del", then the data_node will be
    deleted from this function's records, and the deleted value returned.
    """
    #sdlog.info("JFPFLDAO-280","highest_waiting_priority data_node=%s, cursor=%s" %
    #           (data_node,cursor))
    #sdlog.info("JFPFLDAO-281","highest_waiting_priority.vals=%s" % highest_waiting_priority.vals )
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
            if cursor=="del":  # deprecated
                return highest_waiting_priority.vals.pop(data_node,None)
            hwp0 = SDTimer.get_time() #jfp
            q = "SELECT MAX(priority) FROM file WHERE status='waiting' AND data_node='%s'" % dn
            c.execute(q)
            val = c.fetchone()
            if len(val)>0:
                highest_waiting_priority.vals[dn] = val[0]
            else:
                highest_waiting_priority.vals.pop(dn,None)
            hwp1 = SDTimer.get_elapsed_time( hwp0, show_microseconds=True ) #jfp
            sdlog.info("JFPFLDAO-300","time %s to recompute priority=%s for %s" %
                       (hwp1,val[0],dn) )
            sdlog.info("JFPFLDAO-301","  query %s" % q )
        if cursor==True:
            c.close()
        return (highest_waiting_priority.vals).get(data_nodes[0],None)
#jfp cache in memory: highest_waiting_priority.vals = {}
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
#    upf0 = SDTimer.get_time() #jfp
    keys=['status','error_msg','sdget_status','sdget_error_msg','start_date','end_date','duration','rate','priority']

    # 'url' needs to be present when 'sdnexturl' feature is enabled
    if sdconfig.next_url_on_error:
        keys.append('url')
        keys.append('searchapi_host')

    rowcount=sdsqlutils.update(file,keys,commit,conn)

#    upf1 = SDTimer.get_elapsed_time( upf0, show_microseconds=True ) #jfp
#    sdlog.info("JFPFFDAO-100","update_file time for file %s is %s"%(file.url,upf1))
    # check
    if rowcount==0:
        raise SDException("SYNCDDAO-121","file not found (file_id=%i)"%(i__tr.file_id,))
    elif rowcount>1:
        raise SDException("SYNCDDAO-120","duplicate functional primary key (file_id=%i)"%(i__tr.file_id,))

