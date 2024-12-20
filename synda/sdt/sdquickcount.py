#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.sdt import sdpipeline
from synda.sdt import sdnetutils
from synda.sdt import sdi18n
from synda.sdt import sdcliex
from synda.sdt import sdtypes
from synda.sdt import sdaddap
from synda.sdt import sddeferredbefore
from synda.sdt import sdcommonarg
from synda.sdt.sdexception import SDException

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.api.esgf_search.constants import STRUCTURE as SEARCH_API_STRUCTURE


def run(
        stream=None,
        path=None,
        parameter=[],
        index_host=None,
        dry_run=False,
        type_=SEARCH_API_STRUCTURE['type']['dataset'],
):

    # type management
    if stream is not None:
        sddeferredbefore.add_forced_parameter(stream,'type',type_)
    else:

        # if stream is None, we assume 'parameter' mode
        # (see TAGJFJ4R4JKFFJD for more informations)
        sddeferredbefore.add_forced_parameter(parameter,'type',type_)


    queries=sdpipeline.build_queries(stream=stream,path=path,parameter=parameter,index_host=index_host,parallel=False,load_default=False,count=True)

    if len(queries)<1:
        raise SDException("SDQSEARC-001","No query to process")

    # we don't support multiple queries because of duplicate/intersection between queries
    # (i.e. which num_found attribute to use (from which query..))
    if len(queries)>1:
        raise SDException("SDQSEARC-100","Too much query (multi-query is not allowed in this module, use sdquicksearch instead)")

    query=queries[0]

    if dry_run:
        request=sdtypes.Request(url=query['url'],pagination=False)

        print('%s'%request.get_url())

        # debug
        #print('Url: %s'%request.get_url())
        #print('Attached parameters: %s'%query.get('attached_parameters'))

        return sdtypes.Response()
    else:
        return ws_call(query) # return Response object

def ws_call(query):
    request=sdtypes.Request(url=query['url'],pagination=False)
    result=sdnetutils.call_web_service(request.get_url(),timeout=Preferences().api_esgf_search_http_timeout) # return Response object

    if result.count()>Preferences().api_esgf_search_chunksize:
        raise SDException("SDQSEARC-002","Number of returned files reach maximum limit")

    result=sdaddap.run(result,query.get('attached_parameters',{}))

    return result

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use\n%s"""%sdcliex.search(prog))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-i','--index_host')
    parser.add_argument('-z','--dry_run',action='store_true')

    sdcommonarg.add_type_grp(parser)

    args = parser.parse_args()

    result=run(parameter=args.parameter,index_host=args.index_host,dry_run=args.dry_run,type_=args.type_)

    if not args.dry_run:
        if args.type_==SEARCH_API_STRUCTURE['type']['dataset']:
            print("%i dataset(s) found"%result.num_found)
        elif args.type_==SEARCH_API_STRUCTURE['type']['file']:
            print("%i file(s) found"%result.num_found)
        else:
            print('Not implemented yet')
