#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script set index host (aka search-API service host)."""

import re
import os
import sys
import argparse
import json
import sdapp
import sdindex
import sdlog
import sdprint
import sdstream
import sdtools
import sdpipelineutils

def run(facets_groups,parallel=True,index_host=None,dry_run=False):
    """Set 'searchapi_host' parameter.

    Args:
      facets_groups (list of dict): facets groups
      index_host: index host from arguments (overwrite 'searchapi_host' in facets_groups, if any)

    Notes
        - If 'searchapi_host' parameter is missing both in func arguments and in 'facets_groups', a random index node is used.
        - 'searchapi_host' or 'index_host' is the index host used as url HOST (i.e. the search-API service host where the query will be submitted)
        - 'index_node' is the index host used as url PARAMETER (i.e. the SolR parameter)
    """
    #verbose=sdstream.get_scalar(facets_groups,'verbose',default=False,type_=bool) # we cast here as verbose can be str (set from parameter) or bool (set from '-v' option)
    verbose=False

    for facets_group in facets_groups:

        # index host from args take precedence over one from selection file (if any)
        if index_host is not None:
            facets_group['searchapi_host']=index_host

        # if searchapi_host is set, we force parallel to False
        # (it's not possible to use a specific index in parallel mode so we need to fallback to sequential mode)
        if 'searchapi_host' in facets_group:
            parallel=False

        if dry_run:
            # in dry_run mode, we want searchapi_host to be set, not matter if parallel is enabled or not
            # (i.e. the query is not executed in dry_run mode, we just want to
            # print a working query on stdout, not a query with fake host)

            if 'searchapi_host' not in facets_group:
                facets_group['searchapi_host']=sdindex.get_default_index()
        else:
            if parallel:
                # in parallel mode, we just check that index host is not set (should always be the case)

                assert 'searchapi_host' not in facets_group
            else:
                if 'searchapi_host' not in facets_group:
                    facets_group['searchapi_host']=sdindex.get_default_index()

                #sdlog.debug("SDIDXHST-001","Using %s"%facets_group['searchapi_host'],stderr=False,logfile=True)

                if verbose:
                    sdtools.print_stderr("Using %s"%facets_group['searchapi_host'])

    return facets_groups

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    facets_groups=sdpipelineutils.get_input_data(args.file)
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
