#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module removes file duplicates (e.g. replica).

Notes
    - This module  removes duplicate files in a random way (i.e. all files have the same chance to be removed).
    - This module deals with two types of duplicates (see comments in sdshrink for details).
"""

import sdapp
import sdconst
import sdprint
import sdpostpipelineutils

def run(metadata,mode,keep_replica=False):
    metadata=remove_duplicate(metadata,mode,keep_replica)
    return metadata

def remove_duplicate(metadata,mode,keep_replica):
    """This func remove uniq_id duplicates."""

    files_without_duplicate={}
    for f in files:
        uniq_id=get_uniq_id(f,keep_replica)
        files_without_duplicate[uniq_id]=f # duplicates are removed here (last item in the loop win)

    return files_without_duplicate.values()

def get_uniq_id(f,keep_replica):
    if keep_replica:
        return (sdpostpipelineutils.get_functional_identifier_value(f),f['data_node']) # tuple
    else:
        return sdpostpipelineutils.get_functional_identifier_value(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
