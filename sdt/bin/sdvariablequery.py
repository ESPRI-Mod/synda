#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains variable related SQL queries"""

import argparse
import sdapp
import sddb
import sdconst
from sdtypes import Variable

def get_incomplete_variables():
    """
    This func returns incomplete variable (caused by download error).

    Note
        - This func assumes discovery work with atomic variable
          (i.e. we don't download subset of a variable)
          If not the case, don't use this func.

    DEV
    """
    pass

def get_variables(project='CMIP5'):
    """Return variable list.

    Note
        Variable status is not set here
    """
    variables=[]

    c = sddb.conn.cursor()

    c.execute("select file.project, file.model, file.dataset_id, dataset.path, file.variable from file, dataset where dataset.project=? and file.dataset_id=dataset.dataset_id group by file.project,file.model,file.dataset_id,file.variable",(project,))

    rs=c.fetchone()
    while rs is not None:

        project=rs[0]
        model=rs[1]
        dataset_id=rs[2]
        dataset_path=rs[3]
        variable_name=rs[4]

        variables.append(Variable(project=project,model=model,name=variable_name,dataset_id=dataset_id,dataset_path=dataset_path))

        rs=c.fetchone()

    c.close()

    return variables

def get_variables_files_count_by_status(dataset_id,variable=None):
    """Return how many files with "done" status for each variable of the dataset."""
    variables={}

    c = sddb.conn.cursor()

    if variable is None:
        c.execute("select variable,status,count(*) from file where dataset_id=? group by variable,status",(dataset_id,))
    else:
        c.execute("select variable,status,count(*) from file where dataset_id=? and variable=? group by variable,status",(dataset_id,variable))

    """
    The query returns something like:

    tos|done|3
    tossq|error|2
    """

    rs=c.fetchone()
    while rs is not None:
        v=rs[0]
        status=rs[1]
        count=rs[2]

        if v not in variables:
            variables[v]={status:count}
        else:
            if status not in variables[v]:
                variables[v][status]=count
            else:
                raise SDException("SDSTAQUE-001","Fatal error ('status' should be unique because of the 'group by')")

        rs=c.fetchone()
    c.close()

    # complete with missing statuses (set to 0)
    for v in variables.keys():
        for s in sdconst.TRANSFER_STATUSES_ALL:
            if s not in variables[v]:
                variables[v][s]=0

    return variables

def get_variables_files_count(d):
    """
    return how many files for each variable of the dataset
    """
    variables={}


    c = sddb.conn.cursor()
    c.execute("select variable,count(*) from file where dataset_id=? group by variable",(d.dataset_id,))


    """
    The query returns something like:

    tos|5
    tossq|5
    """

    rs=c.fetchone()
    while rs is not None:

        variable_name=rs[0]
        count=rs[1]

        variables[variable_name]=count
        rs=c.fetchone()
    c.close()

    return variables

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    for v in get_variables():
        print v.dataset_id,v.name
