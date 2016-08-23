#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module filters a list of files."""

import sdapp
from sdexception import SDException
import sdconst
import sdprint
import sdpipelineprocessing

def run(metadata,filter_name,filter_value,mode):
    if mode=='keep':
        po=sdpipelineprocessing.ProcessingObject(keep_matching_files,filter_name,filter_value)
        metadata=sdpipelineprocessing.run_pipeline(metadata,po)
    elif mode=='remove':
        po=sdpipelineprocessing.ProcessingObject(remove_matching_files,filter_name,filter_value)
        metadata=sdpipelineprocessing.run_pipeline(metadata,po)
    else:
        raise SDException("SDSIMPLF-002","Incorrect mode (%s)"%mode)

    return metadata

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
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-m','--mode',required=True)
    parser.add_argument('-s','--status',choices=sdconst.TRANSFER_STATUSES_ALL,required=True)
    args = parser.parse_args()

    files=json.load( sys.stdin )
    metadata=Metadata(files=files)
    metadata=run(metadata,'status',args.status,args.mode)
    sdprint.print_format(metadata.get_files(),args.format,args.print_only_one_item) # warning: load list in memory
