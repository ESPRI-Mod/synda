#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains dataset DAO SQL queries."""

import argparse
import sdapp
from sdexception import SDException
import sddb
import sdsqlutils
from sdtypes import Dataset

def add_dataset(dataset,commit=True,conn=sddb.conn):
    keys_to_insert=['local_path','path','path_without_version','dataset_functional_id','template','version','status','latest','crea_date','last_mod_date','project','model', 'timestamp']
    return sdsqlutils.insert(dataset,keys_to_insert,commit,conn)

def get_dataset_(not_found_raise_exception=False,**search_constraints):
    datasets=get_datasets(**search_constraints)

    if len(datasets)==0:
        if not_found_raise_exception:
            raise SDException("SYNCDDAO-003","Dataset not found")
        else:
            return None
    elif len(datasets)==1:
        return datasets[0]
    else:
        raise SDException("SYNCDDAO-004","Too many results")

def get_dataset(path=None,dataset_id=None,dataset_functional_id=None,conn=sddb.conn):
    """
    TODO: if possible, remove this func and use get_dataset_() instead
    """
    d=None

    c = conn.cursor()

    # Raise exception if having to much search keys
    count=0
    for va in (path,dataset_id,dataset_functional_id):
        if va is not None:
            count=count+1
    if count>1:
        raise SDException("SYNCDDAO-123","Too much arguments (path=%s,dataset_id=%s,dataset_functional_id=%s)"%(path,dataset_id,dataset_functional_id,))

    if path is not None:
        q="select * from dataset where path = '%s'" % path
    elif dataset_id is not None:
        q="select * from dataset where dataset_id = %i" % dataset_id
    elif dataset_functional_id is not None:
        q="select * from dataset where dataset_functional_id = '%s'" % dataset_functional_id
    else:
        raise SDException("SYNCDDAO-124","incorrect arguments")

    c.execute(q)
    rs=c.fetchone()
    if rs is not None:
        d=sdsqlutils.get_object_from_resultset(rs,Dataset)

    c.close()

    return d

def remove_dataset(i__d,commit=True,conn=sddb.conn):
    c = conn.cursor()

    c.execute("delete from dataset where dataset_id=?",(i__d.dataset_id,))

    # check
    if c.rowcount==0:
        raise SDException("SYNCDDAO-229","dataset not found (dataset_id=%s)"%i__d.dataset_id)

    c.close() # note: this does not commit transaction

    if commit:
        conn.commit()

def update_dataset(d,commit=True,conn=sddb.conn,keys=['latest','status','last_mod_date','latest_date','last_done_transfer_date']):
    rowcount=sdsqlutils.update(d,keys,commit,conn)
    
    # check
    if rowcount==0:
        raise SDException("SYNCDDAO-128","dataset not found (dataset_id=%s)"%d.dataset_id)

def exists_dataset(path=None,conn=sddb.conn):
    d=get_dataset(path=path)
    if d is not None:
        return True
    else:
        return False

def get_datasets(limit=None,conn=sddb.conn,**search_constraints): # don't change arguments order here
    """
    Note
        If 'limit' is None, retrieve all records matching the search constraints
    """
    datasets=[]

    c = conn.cursor()

    limit_clause="limit %i"%limit if limit is not None else ""

    if len(search_constraints)>0:
        q="select * from dataset where %s order by path asc %s"%(sdsqlutils.build_search_placeholder(search_constraints),limit_clause)
        c.execute(q,search_constraints)
    else:
        q="select * from dataset order by path asc %s"%limit_clause
        c.execute(q)

    rs=c.fetchone()
    while rs!=None:
        datasets.append(sdsqlutils.get_object_from_resultset(rs,Dataset))
        rs=c.fetchone()

    c.close()

    return datasets

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    args = parser.parse_args()

    if args.dataset is not None:
        #d=get_dataset(dataset_functional_id=args.dataset)
        d=get_dataset_(local_path=args.dataset)
        print d
