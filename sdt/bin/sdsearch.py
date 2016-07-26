#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""ESGF files discovery

This script parse selection file, apply some filters, build search-api
queries, execute queries, apply some filters and print the result.

Notes
 - process only one selection file (aka template) at a time
"""

import os
import argparse
import sdapp
import sdlog
import sdconfig
import sdpipeline
import sdrun
import sdi18n
import sdcliex
import sdprint
import sdconst
import sdtools
import sdsqueries
import sdbatchtimestamp
import sdtypes
from sdexception import SDException,MissingDatasetTimestampUrlException
from sdprogress import ProgressThread

def run(stream=None,selection=None,path=None,parameter=None,post_pipeline_mode='file',parallel=sdconfig.metadata_parallel_download,index_host=None,dry_run=False,load_default=None,lowmem=False):
    """
    Note
        squeries means 'Serialized queries'
    """

    if parameter is None:
        parameter=[]

    squeries=sdpipeline.build_queries(stream=stream,path=path,parameter=parameter,selection=selection,parallel=parallel,index_host=index_host,dry_run=dry_run,load_default=load_default)

    action=sdsqueries.get_scalar(squeries,'action',None)
    progress=sdsqueries.get_scalar(squeries,'progress',False,type_=bool) # we cast here as progress can be str (set from parameter) or bool (set programmaticaly)

    # Prevent use of 'limit' keyword ('limit' keyword can't be used in this module because it interfere with the pagination system)
    for q in squeries:
        if sdtools.url_contains_limit_keyword(q['url']):
            raise SDException('SDSEARCH-001',"'limit' facet is not supported in this mode. Use 'sdquicksearch' module instead.")

    if dry_run:
        sdsqueries.print_(squeries)
        return sdtypes.Metadata()
    else:
        if progress:
            #sdtools.print_stderr(sdi18n.m0003(ap.get('searchapi_host'))) # waiting message
            ProgressThread.start(sleep=0.1,running_message='',end_message='Search completed.') # spinner start

        # retrieve files
        metadata=execute_queries(squeries,parallel,post_pipeline_mode,action)

        if progress:
            ProgressThread.stop() # spinner stop

        return metadata

def execute_queries(squeries,parallel,post_pipeline_mode,action):
    """This func serializes received metadata on-disk to prevent memory overload."""

    sdlog.info("SDSEARCH-580","Retrieve metadata from remote service")
    metadata=sdrun.run(squeries,parallel)
    sdlog.info("SDSEARCH-584","Metadata successfully retrieved (%d files)"%metadata.count())

    sdlog.info("SDSEARCH-590","Metadata processing begin.")

    # way 0: load-all-in-memory
    """
    files=sdpipeline.post_pipeline(metadata.get_files(),post_pipeline_mode) # post-processing
    files=fill_dataset_timestamp(squeries,files,parallel,action) # complete missing info
    metadata.set_files(files)
    """

    # way 1: chunk-by-chunk (using a second store)
    new_metadata=sdtypes.Metadata()
    for chunk in metadata.get_files_GENERATOR():
        files=sdpipeline.post_pipeline(chunk.get_files(),post_pipeline_mode)
        files=fill_dataset_timestamp(squeries,files,parallel,action) # complete missing info
        new_metadata.add(files)
    metadata.delete()
    metadata=new_metadata

    # way 2: chunk-by-chunk (updating store on-the-fly)
    """
    for chunk in metadata.get_files_PAGINATION():
        files=sdpipeline.post_pipeline(chunk.get_files(),post_pipeline_mode)
        files=fill_dataset_timestamp(squeries,files,parallel,action) # complete missing info
        metadata.update(files)
    """

    sdlog.info("SDSEARCH-594","Metadata processing end.")

    return metadata

def fill_dataset_timestamp(squeries,files,parallel,action):

    # HACK
    #
    # second run to retrieve dataset timestamps in one row
    #
    # MEMO: when action is 'install', type is always 'File' (i.e. this code gets executed only for type=File)
    #
    if action is not None:
        if action=='install':
            files=sdbatchtimestamp.add_dataset_timestamp(squeries,files,parallel)

    return files

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""examples of use
  %s -f file
  cat file | %s
%s
"""%(prog,prog,sdcliex.search(prog)))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-f','--file',default=None)
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-i','--index_host')
    parser.add_argument('-m','--post_pipeline_mode',default='file',choices=sdconst.POST_PIPELINE_MODES)
    parser.add_argument('-y','--dry_run',action='store_true')
    parser.add_argument('-1','--print_only_one_item',action='store_true')

    parser.add_argument('--load-default',dest='load_default',action='store_true')
    parser.add_argument('--no-load-default',dest='load_default',action='store_false')
    parser.set_defaults(load_default=None)

    parser.add_argument('--parallel',dest='parallel',action='store_true')
    parser.add_argument('--no-parallel',dest='parallel',action='store_false')
    parser.set_defaults(parallel=True)

    args = parser.parse_args()

    metadata=run(path=args.file,parameter=args.parameter,post_pipeline_mode=args.post_pipeline_mode,dry_run=args.dry_run,load_default=args.load_default,parallel=args.parallel)

    if not args.dry_run:
        sdprint.print_format(metadata.get_files(),args.format,args.print_only_one_item)
