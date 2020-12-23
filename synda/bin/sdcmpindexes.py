#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module is used to check if a selection gives the same result for each ESGF indexes.

Notes
    - This module submit a selection over each indexes and store results for each of them.
    - sdcmpindexes stands for "SynDa compare indexes"
"""

import sys
import os
import argparse
import json
import sdapp
import sdpipeline
import sdindex
import sdrun
import sdprint
import sdproxy_mt

output_dir='/tmp/sdcmpindexes'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('selection_file',nargs='?',default='-',help='Selection file')
    args = parser.parse_args()

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir) 

    queries=sdpipeline.build_queries(path=args.selection_file)

    for index_host in sdindex.index_host_list:
        sdproxy_mt.set_index_hosts([index_host]) # this is to have parallel, but on only one index
        metadata=sdrun.run(queries)
        metadata=sdpipeline.post_pipeline(metadata,'generic') # this is to exclude malformed files if any

        with open('%s/%s'%(output_dir,index_host),'w') as fh:
            sdprint.print_format(metadata.get_files(),'line',fh=fh)
