#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module submit a selection over each indexes and store results for each of them.

This module is used to check if a selection gives the same result for each indexes.

Note
    sdcmpindexes stands for "Synchro-Data compare indexes"
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
    parser.add_argument('file',nargs='?',default='-',help='Selection file')
    args = parser.parse_args()

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir) 

    queries=sdpipeline.build_queries(path=args.file)

    for index_host in sdindex.index_host_list:
        sdproxy_mt.set_index_hosts([index_host]) # this is to have parallel, but on only one index
        files=sdrun.run(queries)
        files=sdpipeline.post_pipeline(files,'generic') # this is to exclude malformed files if any

        with open('%s/%s'%(output_dir,index_host),'w') as fh:
            sdprint.print_format(files,'line',fh=fh)
