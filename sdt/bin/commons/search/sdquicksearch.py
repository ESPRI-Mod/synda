#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This ESGF search module is a light version of sdsearch module which doesn't
contain paging management.

Notes
    - this module cannot retrieve huge number of files (i.e. > 10000)
    - this module cannot be used to count number of matches
    - this module support 'limit' feature
    - this module do not have a next chunk offset based mecanism (i.e. it cannot aggregate multiple search-api calls together)
    - with this module it is NOT possible to retrieve all records if number of result > sdconst.SEARCH_API_CHUNKSIZE
    - this module DO NOT have a retry mecanism if the search-API call failed
    - one advantage of this module is it is not threads based, so
      doing CTRL-C make it stop immediately (but now, it should also be the case
      for sdsearch, as sdproxy_mt threads are now configured as 'daemon')
"""

from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdnetutils
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons import sdi18n
from sdt.bin.commons.utils import sdtools
from sdt.bin.commons.utils import sdprint
from sdt.bin.commons.utils import sdtypes
from sdt.bin.commons.search import sdsqueries
from sdt.bin.commons.search import sdaddap
from sdt.bin.commons.pipeline import sdquerypipeline

from sdt.bin.commons.utils.sdprogress import ProgressThread
from sdt.bin.commons.utils.sdexception import SDException


# TODO simplify quick search call


def run(stream=None, path=None, parameter=None, index_host=None, post_pipeline_mode='file', dry_run=False):
    if parameter is None:
        parameter = []

    queries = build_queries(stream=stream, path=path, parameter=parameter, index_host=index_host,
                            parallel=False, load_default=False)

    if len(queries) < 1:
        raise SDException("SDQSEARC-001", "No query to process")

    # we cast here as progress can be str (set from parameter) or bool (set programmaticaly)
    progress = sdsqueries.get_scalar(queries, 'progress', False, type_=bool)
    searchapi_host = sdsqueries.get_scalar(queries, 'searchapi_host')

    if dry_run:
        for query in queries:
            request = sdtypes.Request(url=query['url'], pagination=False)
            print('{}'.format(request.get_url()))
        return sdtypes.Response()
    else:
        try:
            if progress:
                sdprint.print_stderr(
                    sdi18n.m0003(searchapi_host))  # waiting message => TODO: move into ProgressThread class
                ProgressThread.start(sleep=0.1, running_message='', end_message='Search completed.')  # spinner start

            mqr = process_queries(queries)
            metadata = mqr.to_metadata()

            sdlog.debug("SDQSEARC-002", "files-count={}".format(metadata.count()))
            metadata = sdpipeline.post_pipeline(metadata, post_pipeline_mode)
            sdlog.debug("SDQSEARC-004", "files-count={}".format(metadata.count()))
            return metadata
        finally:
            if progress:
                ProgressThread.stop()  # spinner stop


def build_queries(stream=None, selection=None, path=None, parameter=None, index_host=None, load_default=None,
                  query_type='remote', dry_run=False, parallel=True, count=False):
    """This pipeline add 'path', 'parameter' and 'selection' input type to the standalone query pipeline.
    Returns: squeries (Serialized queries) # TODO: maybe rename stream to dqueries
    """

    if parameter is None:
        parameter = []

    if stream is None:

        if selection is None:
            buffer = sdbuffer.get_selection_file_buffer(path=path, parameter=parameter)
            selection = sdparse.build(buffer, load_default=load_default)

        stream = selection.merge_facets()

    # at this point, stream contains all possible parameters sources (file,stdin,cli..)

    if count:
        # in this mode, we don't want to return any files, so we force limit to
        # 0 just in case this option has been set by the user

        sddeferredafter.add_forced_parameter(stream, 'limit', '0')

    queries = sdquerypipeline.run(stream, index_host=index_host, query_type=query_type, dry_run=dry_run,
                                  parallel=parallel)
    return queries


def process_queries(queries):
    # use RAM to improve speed here (this module is only intended to process small amount of data,
    # so it should be ok on lowmem machine).
    mqr = sdtypes.MultiQueryResponse(lowmen=False)

    for query in queries:
        mqr.slurp(ws_call(query))

    return mqr


def ws_call(query):
    request = sdtypes.Request(url=query['url'], pagination=False)
    # return Response object
    result = sdnetutils.call_web_service(request.get_url(), timeout=sdconst.SEARCH_API_HTTP_TIMEOUT)

    if result.count() >= sdconst.SEARCH_API_CHUNKSIZE:
        raise SDException("SDQSEARC-002", "Number of returned files reach maximum limit")

    result = sdaddap.run(result, query.get('attached_parameters', {}))

    return result
