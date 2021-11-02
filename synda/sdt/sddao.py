#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""Contains SQL simple queries."""
from pandas import DataFrame
from numpy import array
from synda.sdt import sdapp
from synda.sdt import sdconst
from synda.sdt.sdexception import SDException,NoTransferWaitingException,FileNotFoundException
from synda.sdt import sddb
from synda.sdt import sdsqlutils
from synda.sdt import sdtime
from synda.sdt import sdfiledao
from synda.sdt import sddatasetdao

from synda.source.db.connection.models import get_db_connection
from synda.source.config.process.download.constants import TRANSFER
from synda.source.db.task.file.read.models import get_data_nodes

# --- parameter table --- #

def add_parameter_value(name,value,commit=True,conn=sddb.conn):
    ignore_list = ['pid', 'citation_url']
    if name not in ignore_list:
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


def get_one_waiting_transfer(datanode=None):
    if datanode is None:
        li = sdfiledao.get_files(
            limit=1,
            status=TRANSFER["status"]['waiting'],
        )
    else:
        li = sdfiledao.get_files(
            limit=1,
            status=TRANSFER["status"]['waiting'],
            data_node=datanode,
        )

    if len(li) == 0:
        raise NoTransferWaitingException()
    else:
        t = li[0]

    # retrieve the dataset
    d = sddatasetdao.get_dataset(dataset_id=t.dataset_id)
    t.dataset = d

    return t


def get_one_waiting_instance(datanode=None, ascending=True):
    t = None
    conn = get_db_connection()
    if datanode is None:
        li = sdfiledao.get_files(
            status=TRANSFER["status"]['waiting'],
            conn=conn,
        )
    else:
        li = sdfiledao.get_files(
            status=TRANSFER["status"]['waiting'],
            data_node=datanode,
            conn=conn,
        )

    conn.close()

    if len(li) > 0:
        # we must provide instance, fist according to priority before size
        instances = []
        for _li in li:
            instances.append(
                dict(
                    priority=_li.priority,
                    size=_li.size,
                )
            )
        df=DataFrame(instances)
        df = df.sort_values(["priority", "size"], ascending=(False, ascending))
        li = list(array(li)[df.index])
        t = li[0]
        # retrieve the dataset
        d = sddatasetdao.get_dataset(
            dataset_id=t.dataset_id,
        )
        t.dataset = d

    return t


def get_new_tasks(limit=None, datanode=None, ascending=True):
    t = None
    conn = get_db_connection()
    if datanode is None:
        li = sdfiledao.get_files(
            status=TRANSFER["status"]['waiting'],
            conn=conn,
        )
    else:
        li = sdfiledao.get_files(
            status=TRANSFER["status"]['waiting'],
            data_node=datanode,
            conn=conn,
        )

    conn.close()

    if len(li) > 0:
        for _li in li:
            d = sddatasetdao.get_dataset(dataset_id=_li.dataset_id)
            _li.dataset = d
        if ascending:
            li = sdfiledao.sort_by_size_ascending(li)
        else:
            li = sdfiledao.sort_by_size_descending(li)
        if limit:
            li = li[0: limit - 1]
    return li


def get_waiting_downloads():

    downloads = []
    files = sdfiledao.get_files(
        status=TRANSFER["status"]['waiting'],
    )
    if len(files) > 0:
        for _file in files:
            # retrieve the dataset
            d = sddatasetdao.get_dataset(dataset_id=_file.dataset_id)
            _file.dataset = d
            downloads.append(_file)

    return downloads


def check_waiting_files_for_download():

    data_nodes = get_data_nodes()

    unvalidated = []
    validated = []

    for data_node in data_nodes:

        files = sdfiledao.get_files(
            status=TRANSFER["status"]['waiting'],
            data_node=data_node,
        )
        if len(files) > 0:
            files = sdfiledao.sort_by_size_descending(files)
            batch = []
            for _file in files:
                if sdfiledao.validate_for_download(_file):
                    # retrieve the dataset
                    d = sddatasetdao.get_dataset(dataset_id=_file.dataset_id)
                    _file.dataset = d
                    batch.append(_file)
                else:
                    unvalidated.append(_file)
            if len(batch) > 0:
                validated.append(
                    {data_node: batch},
                )

    return validated, unvalidated
