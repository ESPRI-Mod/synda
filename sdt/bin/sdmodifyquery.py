#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains transfers attributes update queries."""

import argparse
import string
import sdapp
import sddb
import sdlog
import sdconst
import sdfiledao

def change_replica(file_functional_id,new_replica,conn=sddb.conn):
    (url,data_node)=new_replica
    sdlog.info("SDMODIFQ-001","Set new replica for %s file (new_url=%s,new_dn=%s)"%(file_functional_id,url,data_node))
    c=conn.cursor()
    res=c.execute("update file set url=?,data_node=? where file_functional_id=?",(url,data_node,file_functional_id))
    conn.commit()
    c.close()

def get_where_clause( where='' ):
    if where=='' or where is None:
        where_clause = ''
    else:
      assert( where.count("'")%2==0 )  # protect against a nasty user error
      assert( where.find('"') )<0  # protect against a nasty user error
      if where.find(' ')>0:
          # arbitrary SQL expression
          where_clause = " AND ("+where+")"
      elif where.find('.')>0:
          # data_node specified
          where_clause = " AND data_node='%s'" % where
      else:
          # data_node substring specified
          where_clause = " AND data_node LIKE %s%s%s" % ("'%",where,"%'")
    return where_clause

def change_status(old_status,new_status,conn=sddb.conn,where=''):
    nbr=0

    where_clause = get_where_clause( where )
    c=conn.cursor()
    res=c.execute(
        "update file set error_msg=NULL,status=?,sdget_error_msg=NULL,sdget_status=NULL WHERE "+\
        "status=?"+where_clause,
        (new_status,old_status,))
    nbr=c.rowcount
    conn.commit()
    if new_status==sdconst.TRANSFER_STATUS_WAITING and sdconst.GET_FILES_CACHING:
        sdfiledao.highest_waiting_priority( True, c )
    c.close()

    return nbr

def change_priority(new_priority,conn=sddb.conn):
    """Change priority value for already existing transfer."""
    c=conn.cursor()
    sdlog.info("SDMODIFQ-002","updating %s selection (new priority=%s)"%(u_s.filename,new_priority))
    res=c.execute("UPDATE file SET priority = ? WHERE EXISTS (SELECT 1 FROM selection__file WHERE file.file_id = selection__file.file_id AND selection__file.selection_id = ?)",(new_priority,u_s.get_selection_id(),))
    modified_files_count=c.rowcount
    conn.commit()
    c.close()

def wipeout_datasets_flags(status=None,latest=0,conn=sddb.conn):
    """Reset flags on all datasets."""
    c=conn.cursor()
    c.execute("update dataset set status=?, latest=?",(status,latest,))
    conn.commit()
    c.close()

def localpath_replace(from_,to,conn=sddb.conn):
    conn.create_function("SUBSTRING_REPLACE", 3, string.replace) # use python as sqlite replace is only available in recent version
    conn.execute("UPDATE file SET local_path=SUBSTRING_REPLACE(local_path,?,?);",(from_,to))
    conn.execute("UPDATE dataset SET local_path=SUBSTRING_REPLACE(local_path,?,?);",(from_,to))
    conn.execute("UPDATE event SET dataset_pattern=SUBSTRING_REPLACE(dataset_pattern,?,?);",(from_,to))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',choices=['local_path_replace'])
    parser.add_argument('from_')
    parser.add_argument('to')
    args = parser.parse_args()

    if args.action=='local_path_replace':
        sdlog.info("SDMODIFQ-100","Modify local_path in metadata (from=%s,to=%s)"%(args.from_,args.to))
        localpath_replace(args.from_,args.to)
        sddb.conn.commit()
    else:
        raise Exception('Incorrect argument(s)')
