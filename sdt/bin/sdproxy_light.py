#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains light routine to access search-api service."""

import sdindex
import sdnetutils
from sdtypes import Request

# FIXME: maybe use get_sample_files() func here
def get_one_file(host=sdindex.get_default_index(),project=None,query=None,dry_run=None):
    """Return one sample file with all attributes."""

    project_filter='' if project is None else "&project=%s"%project
    query_filter='' if query is None else "&query=%s"%query

    url='http://%s/esg-search/search?type=File%s%s&fields=*'%(host,project_filter,query_filter)

    if dry_run:

        print url

        return None

    else:

        # this code cannot use SearchAPIProxy as we need to modify the offset in a non usual way
        request=Request(url=url,pagination=False,limit=50) # limit is arbitrary
        result=sdnetutils.call_web_service(request,60) # return Response object

        # we loop until we find a correct file (i.e. well-formed)
        well_formed_file=None
        for i in range(20): # arbitrary
            for file_ in result.files:
                if len(file_['variable'])==1:
                    well_formed_file=file_
                    break
                else:
                    #print "WARNING: 'variable' attribute contains too much values ('%s')."%file_['title']
                    pass

            if well_formed_file is not None:
                break

            request.offset+=500

            if request.offset<result.num_found:
                result=sdnetutils.call_web_service(request,60) # return Response object
            else:
                break

        return well_formed_file
