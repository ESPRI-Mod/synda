#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module runs queries against the search-API service and returns found files list."""

import sys
import argparse
import json
import sdapp
import sdprint
import sdlog
import sdpipelineutils
import sdproxy_mt
from sdproxy import SearchAPIProxy

def run(queries,parallel=True):
    files=[]

    if parallel:
        (queries_with_index_host,queries_without_index_host)=split_queries(queries) # we need this, because query with specific index host can't be parallelized

        if len(queries_with_index_host)>0:
            files.extend(sequential_exec(queries_with_index_host))

        if len(queries_without_index_host)>0:
            files.extend(parallel_exec(queries_without_index_host))
    else:
        files.extend(sequential_exec(queries))

    return files

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
    return sdproxy_mt.run(queries) # MEMO: sdproxy_mt returns files list

def sequential_exec(queries):
    search=SearchAPIProxy()
    files=[]
    for q in queries:
        result=search.run(url=q['url'],attached_parameters=q.get('attached_parameters')) # MEMO: sdproxy_mt returns Response object
        files.extend(result.files)
    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-')
    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='raw')
    parser.add_argument('-p','--parallel',action='store_true')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    queries=sdpipelineutils.get_input_data(args.file)
    files=run(queries,args.parallel)
    sdprint.print_format(files,args.format,args.print_only_one_item)
