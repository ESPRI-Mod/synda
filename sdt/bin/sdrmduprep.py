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

def run(metadata,functional_id_keyname,keep_replica=False):

    fu=remove_duplicate if keep_replica else remove_duplicate_and_replica

    light_metadata=sdlmattrfilter.run(metadata,['functional_id_keyname','data_node']) # create light list with needed columns only not to overload system memory

    # list of dict => dict of bool
    seen=dict((di[k], False) for di in light_metadata)

    metadata=sdpipelineprocessing.run_pipeline(sdconst.PROCESSING_FETCH_MODE_GENERATOR,metadata,fu,functional_id_keyname,seen)

    return metadata

def remove_duplicate(files,functional_id_keyname,seen):
    new_files=[]
    for f in files:
        uniq_id=(f[functional_id_keyname],f['data_node']) # tuple
        if not seen[uniq]:
            new_files.append(f)
            seen[uniq_id]=True # mark as seen so other duplicate will be excluded (first item in the loop win)
    return new_files

def remove_duplicate_and_replica(files,functional_id_keyname,seen):
    new_files=[]
    for f in files:
        uniq_id=f[functional_id_keyname]
        if not seen[uniq]:
            new_files.append(f)
            seen[uniq_id]=True # mark as seen so other duplicate will be excluded (first item in the loop win)
    return new_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
