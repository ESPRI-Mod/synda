#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains SQL simple queries."""

import sdapp
import sdconst
from sdexception import SDException,NoTransferWaitingException,FileNotFoundException
import sddb
import sdsqlutils
import sdtime
import sdfiledao
import sddatasetdao

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
    c.execute("update selection set checksum=?, status=?  where filename=?",(us.get_checksum(),us.get_status(),us.get_filename()))
    c.close()
    conn.commit()

# --- selection_file_junction table--- #

def insert_selection_file_junction(o,us,commit=True,conn=sddb.conn):
    c = conn.cursor()
    c.execute( "insert into selection__file (file_id,selection_id) values (?,?)",(o.file_id,us.get_selection_id()))
    c.close()

def truncate_selection_transfer_junction(conn=sddb.conn):
    conn.execute("delete from selection__transfer")
    conn.commit()

# --- orphans tables --- #

def truncate_orphan_tables(conn=sddb.conn):
    conn.execute("delete from transfer_without_selection")
    conn.execute("delete from transfer_without_dataset")
    conn.commit()

def insert_transfer_without_selection(t,conn=sddb.conn):
    # no commit here (will be committed in populateselectiontransferjunction()
    c = conn.cursor()
    c.execute("insert into transfer_without_selection (file_id) values (?)",(t.file_id,))
    c.close()

def insert_transfer_without_dataset(t,conn=sddb.conn):
    # no commit here (will be committed in populateselectiontransferjunction()
    c = conn.cursor()
    c.execute("insert into transfer_without_dataset (file_id) values (?)",(t.file_id,))
    c.close()

# --- export table --- #

def store_dataset_export_event(d,conn=sddb.conn):
    c=conn.cursor()
    c.execute("insert into export (dataset_id,export_date) values (?,?)",(d.dataset_id,sdtime.now(),))
    conn.commit()
    c.close()

# --- multi tables --- # 

def get_file(file_functional_id=None):
    li=sdfiledao.get_files(file_functional_id=file_functional_id)

    if len(li)==0:
        raise FileNotFoundException()
    else:
        f=li[0]

    # retrieve the dataset
    d=sddatasetdao.get_dataset(dataset_id=f.dataset_id)
    f.dataset=d

    return f

def get_one_waiting_transfer():
    li=sdfiledao.get_files(limit=1,status=sdconst.TRANSFER_STATUS_WAITING)

    if len(li)==0:
        raise NoTransferWaitingException()
    else:
        t=li[0]

    # retrieve the dataset
    d=sddatasetdao.get_dataset(dataset_id=t.dataset_id)
    t.dataset=d

    return t

# module init.
