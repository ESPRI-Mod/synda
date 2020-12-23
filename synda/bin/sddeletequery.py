#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains queries used by sddeletefile module."""

import sdapp
import sddb
import sdconst

def delete_dataset_transfers(d,conn=sddb.conn):
    """
    mark all transfers for remove (files will be later removed from the local repository by the consumer daemon, and the status will pass to deleted)

    note
      no commit done here !
    """
    c = conn.cursor()
    c.execute("update file set status=? where dataset_id=?",(sdconst.TRANSFER_STATUS_DELETE,d.dataset_id,))
    c.close()

def purge_error_and_waiting_transfer(conn=sddb.conn):
    """
    description
      delete transfer in "error" and "waiting" status

    return
      deleted transfer count
    """
    c = conn.cursor()
    c.execute("delete from selection__file where file_id in (select file_id from file where status in (?,?))",(sdconst.TRANSFER_STATUS_ERROR,sdconst.TRANSFER_STATUS_WAITING))
    c.execute("delete from file where status in (?,?)",(sdconst.TRANSFER_STATUS_ERROR,sdconst.TRANSFER_STATUS_WAITING))
    nbr=c.rowcount
    c.close()
    conn.commit()

    return nbr

def purge_orphan_datasets(conn=sddb.conn):
    c = conn.cursor()
    c.execute("delete from dataset where not exists (select 1 from file where dataset.dataset_id = file.dataset_id)")
    nbr=c.rowcount
    c.close()
    conn.commit()
    return nbr

