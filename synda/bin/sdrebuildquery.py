#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains rebuild queries."""

import sdapp
import sddb
from sdexception import SDException

def update_model_names(conn=sddb.conn):
    """
    fix B0032 (set non_normalized_model_name)
    """
    sdlog.info("SDREBUQU-832","updating model names..")

    c = conn.cursor()

    for non_normalized_model_name in CESGFParametersRetriever.getESGFParams_SEARCHAPI(param_name="model"):
        normalized_model_name=CDRS.normalizeModelName(non_normalized_model_name)

        c.execute("update model set non_normalized_name = ? where name = ?",(non_normalized_model_name,normalized_model_name))

        conn.commit()

    c.close()

def get_transfers__variable_null(conn=sddb.conn):
    list=[]
    c = conn.cursor()

    q="select %s from transfer where variable is null limit 1000" % sddao.transfer_columns
    c.execute(q)

    rs=c.fetchone()
    while rs!=None:
        list.append(sddao.getTransferFromResultSet(rs))
        rs=c.fetchone()

    c.close()

    return list

def update_dataset(d,conn=sddb.conn):
    c = conn.cursor()

    c.execute("update dataset set model=? where dataset_id=?",(d.getModel(),d.dataset_id,))

    # check
    if c.rowcount==0:
        raise SDException("SDREBUQU-828","dataset not found (dataset_id=%s)"%d.dataset_id)

    c.close() # note: this does not commit transaction

    conn.commit()
