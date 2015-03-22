#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sddao.py 3049 2014-02-09 15:52:49Z jripsl $
#  @version        $Rev: 3049 $
#  @lastrevision   $Date: 2014-02-09 16:52:49 +0100 (Sun, 09 Feb 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains SQL simple queries."""

import sdapp
from sdexception import SDException
import sddb
import sdsqlutils
import sdtime

# --- version table --- #

def get_version():
    c = conn.cursor()
    c.execute("select version from version")
    rs=c.fetchone()

    if rs==None:
        raise SDException("SYNCDDAO-316","fatal error")

    version=rs[0]

    c.close()

    return version

def update_version(version):
    c = conn.cursor()
    c.execute("update version set version=?",(version,))
    conn.commit()
    c.close()

# --- parameter table --- #

def add_parameter_value(name,value,commit=True,conn=sddb.conn):
    conn.execute("insert into param (name,value) values (?,?)",(name,value))
    if commit:
        conn.commit()

def fetch_parameters(conn=sddb.conn):
    """Retrieve all parameters

    Returns:
        params (dict)
    """
    params={}

    c = conn.cursor()
    c.execute("select name,value from param")
    rs=c.fetchone()
    while rs!=None:
        name=rs[0]
        value=rs[1]

        if name in params:
            params[name].append(value)
        else:
            params[name]=[]
            params[name].append(value)

        rs=c.fetchone()
    c.close()

    return params

def exists_parameter_value(name,value,conn=sddb.conn):
    c = conn.cursor()
    c.execute("select count(1) from param where name = ? and value = ?",(name,value,))
    rs=c.fetchone()
    count=rs[0]
    c.close()
    if count==1:
        return True
    elif count==0:
        return False
    else:
        raise SDException("SYNCDDAO-829","fatal error")

def exists_parameter_name(name,conn=sddb.conn):
    c = conn.cursor()
    c.execute("select count(1) from param where name = ?",(name,))
    rs=c.fetchone()
    count=rs[0]
    c.close()
    if count>0:
        return True
    else:
        return False

# --- selection table --- #

def fetch_selection(filename,conn=sddb.conn):
    us=None

    c = conn.cursor()
    c.execute("select selection_id, filename, checksum, status from selection where filename = ?",(filename,))

    rs=c.fetchone()

    if rs is not None:
        us=CSelection(selection_id=rs[0],filename=rs[1],checksum=rs[2],status=rs[3],loadselectionparameterfromfile=False)

    c.close()

    return us

def exists_selection(us):
    if fetch_selection(us.filename) is None:
        return False
    else:
        return True

def insert_selection(us,conn=sddb.conn):
    """
    warning: this method modify "us" object
    """
    c = conn.cursor()

    c.execute("insert into selection (filename, checksum, status) values (?,?,?)",(us.filename,us.checksum,us.status))
    us.selection_id=c.lastrowid # set PK
    c.close()

    conn.commit()

def update_selection(us,conn=sddb.conn):
    c = conn.cursor()
    c.execute("update selection set checksum=?, status=?  where filename=?",(us.getChecksum(),us.getStatus(),us.getFilename()))
    c.close()
    conn.commit()

# --- selection_file_junction table--- #

def insert_selection_file_junction(o,us,commit=True,conn=sddb.conn):
    c = conn.cursor()
    c.execute( "insert into selection__file (file_id,selection_id) values (?,?)",(o.file_id,us.getSelectionID()))
    c.close()

def truncate_selection_transfer_junction(conn=sddb.conn):
    conn.execute("delete from selection__transfer")
    conn.commit()

# --- history table --- #

def add_history_line(action,selection_filename=None,insertion_group_id=None,conn=sddb.conn):
    c = conn.cursor()
    c.execute("insert into history (action, selection_filename, crea_date, insertion_group_id) values (?,?,?,?)",(action, selection_filename, sdtime.now(), insertion_group_id))
    c.close()
    conn.commit()

def get_history_lines(conn=sddb.conn):
    li=[]
    c = conn.cursor()
    c.execute("select action,crea_date,selection_filename,insertion_group_id from history")
    rs=c.fetchone()
    while rs!=None:
        li.append(sdsqlutils.resultset_to_dict(rs))
        rs=c.fetchone()
    c.close()
    return li

# --- orphans tables --- #

def truncate_orphan_tables(conn=sddb.conn):
    conn.execute("delete from transfer_without_selection")
    conn.execute("delete from transfer_without_dataset")
    conn.commit()

def insert_transfer_without_selection(t,conn=sddb.conn):
    # no commit here (will be committed in populateSelectionTransferJunction()
    c = conn.cursor()
    c.execute("insert into transfer_without_selection (file_id) values (?)",(t.file_id,))
    c.close()

def insert_transfer_without_dataset(t,conn=sddb.conn):
    # no commit here (will be committed in populateSelectionTransferJunction()
    c = conn.cursor()
    c.execute("insert into transfer_without_dataset (file_id) values (?)",(t.file_id,))
    c.close()

# --- export table --- #

def store_dataset_export_event(d,conn=sddb.conn):
    c=conn.cursor()
    c.execute("insert into export (dataset_id,export_date) values (?,?)",(d.dataset_id,sdtime.now(),))
    conn.commit()
    c.close()

# module init.
