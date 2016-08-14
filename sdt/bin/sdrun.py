#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module runs queries against the search-API service and returns found files list.

Notes
    - Do not use parallel mode on low memory machine
      (else many huge buffer are likely to be open simultaneously in sdnetutils.call_web_service)
      use sequential mode instead.
    - This module can be tested with
      cat selection_4.txt | sdquerypipeline.py -i esgf-node.ipsl.upmc.fr | sdrun.py -f indent
"""

import sys
import argparse
import json
import sdapp
import sdprint
import sdlog
import sdpipelineutils
import sdproxy_mt
import sdtypes
import sdproxy

def run(queries,parallel=True):

    if parallel:
        metadata=sdtypes.Metadata()

        (queries_with_index_host,queries_without_index_host)=split_queries(queries) # we need this, because query with specific index host can't be parallelized

        if len(queries_with_index_host)>0:
            metadata.slurp(sequential_exec(queries_with_index_host))

        if len(queries_without_index_host)>0:
            metadata.slurp(parallel_exec(queries_without_index_host))
    else:
        metadata=sequential_exec(queries)

    return metadata

def split_queries(queries):
    queries_with_index_host=[]
    queries_without_index_host=[]

    for q in queries:
        if is_index_host_set(q):
            # query must be run on a specified index

            queries_with_index_host.append(q)
        else:
            # query can be run on any indexes

            queries_without_index_host.append(q)

    return (queries_with_index_host,queries_without_index_host)

def is_index_host_set(query):
    """
    Returns:
        True: index host is set
        False:  index host is set
    """
    if 'attached_parameters' in query:
        if 'searchapi_host' in query['attached_parameters']:
            return True
        else:
            return False
    else:
        return False

def parallel_exec(queries):
    return sdproxy_mt.run(queries)

def sequential_exec(queries):
    search=sdproxy.SearchAPIProxy()
    metadata=sdtypes.Metadata()
    for i,q in enumerate(queries):
        sdlog.info("SYNDARUN-001","Process query %d"%i)
        result=search.run(url=q['url'],attached_parameters=q.get('attached_parameters'))
        metadata.slurp(result)
    return metadata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-p','--parallel',action='store_true')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    queries=sdpipelineutils.get_input_data(args.file)
    metadata=run(queries,args.parallel)
    files=metadata.get_files() # warning: load list in memory
    sdprint.print_format(files,args.format,args.print_only_one_item)
