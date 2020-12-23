#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains SQL utils."""

import re
import argparse
import sdapp
from sdexception import SDException
import sddb
import sdlog
import sdconst
import sqlite3
import pdb

def sql_injection_safe(s):
    regex=r'[^a-zA-Z0-9_]'
    match=re.search(regex,s)
    if match!=None:
        return False
    else:
        return True

def get_object_from_resultset(rs,class_):
    kw=resultset_to_dict(rs)
    return class_(**kw)

def get_tablename(o):
    # beware: this method works only if the object name is the same as the table name (case excluded)

    return o.__class__.__name__.lower() # (e.g. File gives "file")

def build_search_placeholder(search_constraints):
    return " AND ".join(["%s=:%s"%(k,k) if search_constraints[k] is not None else "%s IS NULL"%k for k in search_constraints])

def resultset_to_dict(rs):
    # TODO: is this method needed ?

    kw={}
    for column in rs.keys():
        kw[column]=rs[column]
    return kw

def truncate_table(table,conn=sddb.conn):
    conn.execute("delete from %s"%table)
    conn.commit()

def truncate_part_of_table(table,col,pattern,conn=sddb.conn):
    conn.execute("delete from %s where %s like '%s'"%(table,col,pattern))
    conn.commit()

def truncate_errorfiles_failed_url(conn=sddb.conn):
    """This does just one job: delete from the failed_url table where the matching file table
    has status='error'"""
    cmd = "DELETE FROM failed_url WHERE url IN (SELECT failed_url.url FROM failed_url INNER JOIN"+\
          " file ON failed_url.url LIKE '%s'||file.filename AND file.status='%s')" %\
          ("%",sdconst.TRANSFER_STATUS_ERROR)
    conn.execute(cmd)
    conn.commit()

def nextval(col,tbl):
    """Return next value for column given in argument."""
    max_id=None
    conn=sddb.conn
    c = conn.cursor()
    c.execute("select max(%s) from %s"%(col,tbl))
    rs=c.fetchone()

    assert rs<>None
    assert len(rs)==1

    if rs[0] is not None:
        max_id=rs[0]+1
    else:
        max_id=1

    c.close()

    return max_id

def insert(instance,columns_subset,commit,conn):
    """This func insert data in table using placeholders.

    Note:
        If columns_subset is None, all instance members are inserted.
    """
    def get_dict(instance,keys):
        d={}
        if keys is None:
            d=instance.__dict__
        else:
            for k in keys:
                d[k]=instance.__dict__[k]

        return d
    def do_insert( query, d, conn ):
        c = conn.cursor()
        c.execute(query, d) # placeholders resolution take place here
        id_=c.lastrowid
        c.close()
        return id_

    # create dict containing key/val list to be inserted
    d=get_dict(instance,columns_subset)

    # generate SQL
    tablename=get_tablename(instance)
    columns=', '.join(d.keys())
    placeholders=':'+', :'.join(d.keys())
    query='INSERT INTO %s (%s) VALUES (%s)' % (tablename,columns, placeholders)

    # EXEC
    try:
        id_ = do_insert( query, d, conn )
    except sqlite3.IntegrityError as e:
        # This sometimes happens due to errors in which, at the data node, one dataset shared its
        # location with another one; or in which the same file is published in two locations.
        # The log output should provide enough information to diagnose the problem.
        sdlog.info("SDSQLUTI-001",("During database operations, IntegrityError %s from\n   "+
                   "tablename=%s,\n   columns=%s,\n   placeholders=%s\n   with dict %s")
                   %(e,tablename,columns,placeholders,d))
        try:
            d['status'] = sdconst.TRANSFER_STATUS_PATH_ERROR
            d['local_path'] = d['local_path']+'_bad_path_'+str(d['checksum'])+str(d['crea_date'])
            d['file_functional_id'] = d['file_functional_id']+'_bad_path_'+str(d['checksum'])+\
                str(d['crea_date'])
            id_ = do_insert( query, d, conn )
        except sqlite3.IntegrityError:
            raise

    if commit:
        conn.commit()

    return id_

def update(instance,columns_subset_without_pk,commit,conn):
    """This func update data in table using placeholders.

    Note:
        - If 'columns_subset_without_pk' is None, all instance members are updated.
    """

    def get_dict(instance,keys,pkname):
        d_without_pk={}

        for k in keys:
            d_without_pk[k]=instance.__dict__[k]

        d_with_pk={pkname:instance.__dict__[pkname]}
        d_with_pk.update(d_without_pk)

        return (d_with_pk,d_without_pk)


    tablename=get_tablename(instance)
    pk=tablename+'_id'

    # create dict containing key/val list to be updated
    (d_with_pk,d_without_pk)=get_dict(instance,columns_subset_without_pk,pk)

    # generate SQL
    pk_placeholders='%s=:%s'%(pk,pk)
    payload_placeholders=', '.join(['%s=:%s'%(k,k) for k in d_without_pk.keys()])
    query='UPDATE %s SET %s WHERE %s' % (tablename, payload_placeholders,pk_placeholders)

    # debug
    #print query
    #print d_with_pk
    #return

    # EXEC
    c = conn.cursor()
    c.execute(query, d_with_pk) # placeholders resolution take place here
    rowcount=c.rowcount
    c.close()

    if commit:
        conn.commit()

    return rowcount

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('teststring')
    args = parser.parse_args()

    #print nextval('insertion_group_id','file')
    print sql_injection_safe(args.teststring)
