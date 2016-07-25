#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module is used to count how many match exist in ESGF for a given set of filters.

Notes
    - This module is the same as sdquicksearch module except for the points below
        - it doesn't support multi-query
        - it returns Reponse object, which contains the 'num_found' attribute
          (used to count to number of match in ESGF)
    - see sdquicksearch notes for more infos
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
import sdcliex
import sdprint
import sdsqueries
from sdprogress import ProgressThread
import sdtypes
from sdexception import SDException

def run(stream=None,path=None,parameter=[],index_host=None,post_pipeline_mode='file',dry_run=False):
    queries=sdpipeline.build_queries(stream=stream,path=path,parameter=parameter,index_host=index_host,parallel=False,load_default=False,count=True)

    if len(queries)<1:
        raise SDException("SDQSEARC-001","No query to process")

    if len(queries)>1:
        raise SDException("SDQSEARC-100","Too much query (multi-query is not allowed in this module, use sdquicksearch instead)")

    progress=sdsqueries.get_scalar(queries,'progress',False,type_=bool) # we cast here as progress can be str (set from parameter) or bool (set programmaticaly)
    searchapi_host=sdsqueries.get_scalar(queries,'searchapi_host')


    if dry_run:
        for query in queries:
            request=sdtypes.Request(url=query['url'],pagination=False)

            print '%s'%request.get_url()

            # debug
            #print 'Url: %s'%request.get_url()
            #print 'Attached parameters: %s'%query.get('attached_parameters')

        return sdtypes.Response()
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
    query=queries[0] 
    return ws_call(query)

def ws_call(query):
    request=sdtypes.Request(url=query['url'],pagination=False)
    result=sdnetutils.call_web_service(request.get_url(),sdconst.SEARCH_API_HTTP_TIMEOUT) # return Response object

    if result.num_result>=sdconst.CHUNKSIZE:
        raise SDException("SDQSEARC-002","Number of returned files reach maximum limit")

    result.add_attached_parameters(query.get('attached_parameters',{}))
    return result

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use\n%s"""%sdcliex.search(prog))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-i','--index_host')
    parser.add_argument('-m','--post_pipeline_mode',default='file')
    parser.add_argument('-y','--dry_run',action='store_true')

    args = parser.parse_args()

    result=run(parameter=args.parameter,index_host=args.index_host,post_pipeline_mode=args.post_pipeline_mode,dry_run=args.dry_run)

    print "%i"%result.num_found
