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

import sdapp
import sddb
import sdlog

def change_replica(file_functional_id,new_replica,conn=sddb.conn):
    (url,data_node)=new_replica
    sdlog.info("SDMODIFQ-001","Set new replica for %s file (new_url=%s,new_dn=%s)"%(file_functional_id,url,data_node))
    c=conn.cursor()
    res=c.execute("update file set url=?,data_node=? where file_functional_id=?",(url,data_node,file_functional_id))
    conn.commit()
    c.close()

def change_status(old_status,new_status,conn=sddb.conn):
    nbr=0

    c=conn.cursor()
    res=c.execute("update file set error_msg=NULL,status=?,sdget_error_msg=NULL,sdget_status=NULL where status=?",(new_status,old_status,))
    nbr=c.rowcount
    conn.commit()
    c.close()

    return nbr

def change_priority(new_priority,conn=sddb.conn):
    """Change priority value for already existing transfer."""
    c=conn.cursor()
    sdlog.info("SDMODIFQ-002","updating %s selection (new priority=%s)"%(u_s.filename,new_priority))
    res=c.execute("UPDATE file SET priority = ? WHERE EXISTS (SELECT 1 FROM selection__file WHERE file.file_id = selection__file.file_id AND selection__file.selection_id = ?)",(new_priority,u_s.getSelectionID(),))
    modified_files_count=c.rowcount
    conn.commit()
    c.close()

def reset_datasets_flags(conn=sddb.conn):
    """Reset flags on all datasets."""
    c=conn.cursor()
    c.execute("update dataset set status=?, latest=?",(None,0,))
    conn.commit()
    c.close()
