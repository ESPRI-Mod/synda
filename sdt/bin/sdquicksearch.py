#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This ESGF search module is a light version of sdsearch module which doesn't
contain paging management.

Notes
    - this module cannot retrieve huge number of files (i.e. > 10000)
    - this module can be used to count number of matches
    - this module support 'limit' feature
    - this module do not have a next chunk offset based mecanism (i.e. it cannot aggregate multiple search-api calls together)
    - with this module it is NOT possible to retrieve all records if number of result > sdconst.CHUNKSIZE
    - this module DO NOT have a retry mecanism if the search-API call failed
    - one advantage of this module is it is not threads based, so
      doing CTRL-C make it stop immediately (but now, it should also be the case
      for sdsearch, as sdproxy_mt threads are now configured as 'daemon')
"""

import os
import argparse
import json
import sdapp
import sdtools
import sdpipeline
import sdconst
import sdconfig
import sdnetutils
import sdi18n
import sdprint
import sdsqueries
from sdprogress import ProgressThread
from sdtypes import Request,Response
from sdexception import SDException

def run(stream=None,path=None,parameter=[],index_host=None,post_pipeline_mode='file',dry_run=False,count=False):
    queries=sdpipeline.build_queries(stream=stream,path=path,parameter=parameter,index_host=index_host,parallel=False,load_default=False,count=count)

    if len(queries)<1:
        raise SDException("SDQSEARC-001","No query to process")

    progress=sdsqueries.get_scalar(queries,'progress',False,type_=bool) # we cast here as progress can be str (set from parameter) or bool (set programmaticaly)
    searchapi_host=sdsqueries.get_scalar(queries,'searchapi_host')


    if dry_run:
        for query in queries:
            request=Request(url=query['url'],pagination=False)

            print '%s'%request.get_url()

            # debug
            #print 'Url: %s'%request.get_url()
            #print 'Attached parameters: %s'%query.get('attached_parameters')

        return Response()
    else:
        try:
            if progress:
                sdtools.print_stderr(sdi18n.m0003(searchapi_host)) # waiting message => TODO: move into ProgressThread class
                ProgressThread.start(sleep=0.1,running_message='',end_message='Search completed.') # spinner start

            result=process_queries(queries) # return Response object

            # post-call-processing
            result.files=sdpipeline.post_pipeline(result.files,post_pipeline_mode)
            result.num_result=len(result.files) # sync objec attributes (yes, maybe not the best place to do that). We do that because sdpipeline.post_pipeline() method is likely to change the number of items in 'files' attribute (i.e. without updating the corresponding 'num_result' attribute, so we need to do it here).

            return result
        finally:
            if progress:
                ProgressThread.stop() # spinner stop

def process_queries(queries):
    if len(queries)>1:
        total_result=Response()
        total_result.call_duration=0 # we need to do this for the sum operation below not to raise exception (MEMO: call_duration is None by default).

        for query in queries:
            result=ws_call(query)
            total_result.files.extend(result.files)
            total_result.call_duration+=result.call_duration # have sense, because is sequential

        total_result.num_found=None # this number have no more meaning/sense with multiple queries (i.e. because of duplicate/intersection between queries)
        total_result.num_result=len(total_result.files)

        return total_result
    else:
        query=queries[0] 
        result=ws_call(query)
        return result

def ws_call(query):
    request=Request(url=query['url'],pagination=False)
    result=sdnetutils.call_web_service(request,sdconst.SEARCH_API_HTTP_TIMEOUT) # return Response object

    if result.num_result>=sdconst.CHUNKSIZE:
        raise SDException("SDQSEARC-002","Number of returned files reach maximum limit")

    result.add_attached_parameters(query.get('attached_parameters',{}))
    return result

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use\n%s"""%sdi18n.m0002(prog))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-c','--count',action='store_true',help='Count how many found files')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='indent')
    parser.add_argument('-i','--index_host')
    parser.add_argument('-m','--post_pipeline_mode',default='file')
    parser.add_argument('-y','--dry_run',action='store_true')
    parser.add_argument('-1','--print_only_one_item',action='store_true')

    args = parser.parse_args()

    result=run(parameter=args.parameter,index_host=args.index_host,post_pipeline_mode=args.post_pipeline_mode,dry_run=args.dry_run,count=args.count)

    if args.count:
        print "%i"%result.num_found
    else:
        sdprint.print_format(result.files,args.format,args.print_only_one_item)
