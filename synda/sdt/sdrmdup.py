#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module removes file duplicates.

Notes
    - This module removes duplicate files in a random way (i.e. all files have the same chance to be removed).
    - This module keeps replicates
    - sdrmdup means 'SynDa ReMove DUPlicate'

See also
    - sdshrink
"""

from synda.sdt import sdapp
from synda.sdt import sdconst
from synda.sdt import sdprint
from synda.sdt import sdpostpipelineutils
from synda.sdt import sdlmattrfilter
from synda.sdt import sdpipelineprocessing

def run(metadata,functional_id_keyname):
    light_metadata=sdlmattrfilter.run(metadata,[functional_id_keyname,'data_node']) # create light list with needed columns only not to overload system memory

    # list of dict => dict (id=>bool)
    seen=dict(((f[functional_id_keyname],f['data_node']), False) for f in light_metadata.get_files())

    po=sdpipelineprocessing.ProcessingObject(remove,functional_id_keyname,seen)
    metadata=sdpipelineprocessing.run_pipeline(metadata,po)

    return metadata

def remove(files,functional_id_keyname,seen):
    new_files=[]
    for f in files:
        uniq_id=(f[functional_id_keyname],f['data_node']) # tuple
        if not seen[uniq_id]:
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
