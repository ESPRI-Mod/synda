#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module filters a list of files."""

import sdapp
from sdexception import SDException
import sdconst
import sdprint

def run(files,filter_name,filter_value,mode):
    if mode=='keep':
        return keep_matching_files(files,filter_name,filter_value)
    elif mode=='remove':
        return remove_matching_files(files,filter_name,filter_value)
    else:
        raise SDException("SDSIMPLF-002","Incorrect mode (%s)"%mode)

def keep_matching_files(files,filter_name,filter_value):
    """Keeps files with a match.

    Note:
        - If filter name not found in file attributes, raises exception.
    """
    new_files=[]
    for f in files:

        if filter_name not in f:
            raise SDException("SDSIMPLF-001","Filter name not found in file attributes (filter_name=%s)"%(filter_name,))

        if f[filter_name]==filter_value:
            new_files.append(f)

    files=new_files

    return files

def remove_matching_files(files,filter_name,filter_value):
    """Remove files with a match.

    Note:
        If filter name not found in file attributes, raises exception.
    """
    new_files=[]
    for f in files:

        if filter_name not in f:
            raise SDException("SDSIMPLF-003","Filter name not found in file attributes (filter_name=%s)"%(filter_name,))

        if f[filter_name]!=filter_value:
            new_files.append(f)

    files=new_files

    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    parser.add_argument('-m','--mode',required=True)
    parser.add_argument('-s','--status',choices=sdconst.TRANSFER_STATUSES_ALL,required=True)
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files,'status',args.status,args.mode)
    sdprint.print_format(files,args.format,args.print_only_one_item)
