#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains variable utils."""

import argparse
import re
import sdapp
import sdconst
import sdlog
from sdtypes import Variable
import sdvariablequery

def build_variable_functional_id(dataset_functional_id,v):
    """Note that this is NOT an ESGF official identifier.

    Input sample
        cmip5.output1.BCC.bcc-csm1-1-m.rcp26.day.atmos.day.r1i1p1.20120910
    """

    # basic format (variable and dataset_functional_id are separated by space char)
    #variable_functional_id='%s %s'%(dataset_functional_id,v)

    # aggregation format 
    #
    # e.g. 
    #  - cmip5.output1.BCC.bcc-csm1-1-m.rcp26.day.atmos.day.r1i1p1.clt.20120910
    #  - cmip5.output1.BCC.bcc-csm1-1-m.rcp26.day.atmos.day.r1i1p1.clt.20120910.aggregation
    #
    variable_functional_id=re.sub('^(.*)\.([^.]+)$', "\\1.%s.\\2.aggregation"%v, dataset_functional_id)

    return variable_functional_id

def exists_one_complete_variable(d):
    """Return true if the dataset contains at least one variable with all transfer done, else False."""

    vars_files_count=sdvariablequery.get_variables_files_count(d)
    vars_files_count_by_status=sdvariablequery.get_variables_files_count_by_status(d.dataset_id)

    for k in vars_files_count_by_status.keys(): # k => varname

        done_count=vars_files_count_by_status[k][sdconst.TRANSFER_STATUS_DONE]

        if vars_files_count[k]==done_count: # is the number of done files same as the number of all files, for this variable ? (if true, means that all variable files are done)
            return True

    return False

def is_variable_complete(dataset_id,variable):
    di=sdvariablequery.get_variables_files_count_by_status(dataset_id,variable)

    if variable in di:

        total=sum(count for count in di[variable].values())

        if total==di[variable][sdconst.TRANSFER_STATUS_DONE]:
            # all done (total nbr of files same as nbr of done files)
            return True
        else:
            return False

    else:
        # variable doesn't exist for this dataset

        # We return true in this case.
        # I.e. we consider that all files are complete as there is no file at all.
        # Doing this makes things a lot simpler in sdevent module.
        #
        return True

def get_variables_progress(d):
    """Return dict with a status (progress information) for each variable of the dataset."""
    vars=[]

    vars_files_count=sdvariablequery.get_variables_files_count(d)
    vars_files_count_by_status=sdvariablequery.get_variables_files_count_by_status(d.dataset_id)

    for k,v in vars_files_count.items(): # k => varname, v => count
        if k in vars_files_count_by_status:
            if vars_files_count_by_status[k][sdconst.TRANSFER_STATUS_DONE]==v: # is the number of done files same as the number of all files, for this variable ? (if true, means that all variable files are done)
                vars.append(Variable(name=k,status=sdconst.VARIABLE_COMPLETE))
            else:
                vars.append(Variable(name=k,status=sdconst.VARIABLE_NOT_COMPLETE))
        else:
            vars.append(Variable(name=k,status=sdconst.VARIABLE_NOT_COMPLETE))

    return vars

def get_complete_variables(project='CMIP5'):
    complete_vars=[]
    for v in sdvariablequery.get_variables(project=project):
        if is_variable_complete(v.dataset_id,v.name):
            complete_vars.append(v)
    return complete_vars

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dataset_id',type=int,required=True)
    parser.add_argument('-v','--variable',required=True)
    args = parser.parse_args()

    print is_variable_complete(args.dataset_id,args.variable)
