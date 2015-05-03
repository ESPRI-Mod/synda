#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains "query" pipeline's jobs."""

import re
import os
import sys
import argparse
import sdapp
import sdparse
import sdexplode
import sdremoteqbuilder
import sdlocalqbuilder
import sdbuffer
import sdcompletedatasetid
import sdindexhost
import sdremote2local
from sdexception import SDException
import sdnearestpre
import sdparampipeline
import sdtps
import sdonemgf_pre
import sdconfig
import sdprint

def run(facets_groups,parallel=True,index_host=None,dry_run=False,query_type='remote'):
    facets_groups=sdparampipeline.run(facets_groups)

    if query_type=='remote':
        #facets_groups=sdcompletedatasetid.run(facets_groups) # beware: this trigger a search-api call
        facets_groups=sdonemgf_pre.run(facets_groups,dry_run=False)
        facets_groups=sdindexhost.run(facets_groups,parallel=parallel,index_host=index_host,dry_run=dry_run)
        #facets_groups=sdexplode.run(facets_groups) # ,facet_to_explode='filename'

        # experimental
        if sdconfig.nearest_schedule=='pre':
            facets_groups=sdexplode.run(facets_groups) # maybe this is not needed (to be confirmed)
            facets_groups=sdnearestpre.run(facets_groups)

        if sdconfig.twophasesearch:
            facets_groups=sdtps.run(facets_groups) # two phase search

        queries=sdremoteqbuilder.run(facets_groups)
    elif query_type=='local':
        facets_groups=sdremote2local.run(facets_groups)
        queries=sdlocalqbuilder.run(facets_groups)
    else:
        raise SDException("SDQUERYP-001","Unknow query type (%s)"%query_type)

    return queries

if __name__ == '__main__':
    prog=os.path.basename(__file__)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""examples of use
  cat file | %s
  %s file
"""%(prog,prog))

    parser.add_argument('file',nargs='?',default='-')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    parser.add_argument('-i','--index_host')

    parser.add_argument('--parallel',dest='parallel',action='store_true')
    parser.add_argument('--no-parallel',dest='parallel',action='store_false')
    parser.set_defaults(parallel=True)

    args = parser.parse_args()

    buffer=sdbuffer.get_selection_file_buffer(path=args.file)
    selection=sdparse.build(buffer)
    facets_groups=selection.merge_facets()
    queries=run(facets_groups,parallel=args.parallel,index_host=args.index_host)

    sdprint.print_format(queries,args.format,args.print_only_one_item)
