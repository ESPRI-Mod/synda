#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script builds search-API query from search-API facets.

Url samples
    - http://<host>/esg-search/search?project=GeoMIP&type=File&experiment=G1&variable=rsdt&fields=*&latest=true

Note
    - 'sdremoteqbuilder' means 'SynDa remote Query builder'

Reference
    - https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API
"""

import argparse
import sdapp
import sdconst
import sdlog
import sddquery
import sdpipelineutils
import sdremotequtils
import sdprint

def run(facets_groups):
    queries=[]

    for facets_group in facets_groups:

        query=build_query(facets_group)
 
        queries.append(query)

    return queries

def build_url(facets,searchapi_host):
    url=sdremotequtils.build_url(facets)

    if searchapi_host is not None:
        url=url.replace(sdconst.IDXHOSTMARK,searchapi_host)
    else:
        # we leave the fake index host (it will be replaced with the real host later)

        pass

    return url

def build_query(facets_group):

    assert(isinstance(facets_group,dict))


    # set default type
    if 'type' not in facets_group:
        facets_group['type']=['File'] # set as list (all Search-API facets are list at this point)

    # if 'fields' not set, we retrieve all attributes
    if 'fields' not in facets_group:
        facets_group['fields']=['*']


    searchapi_host=facets_group.get('searchapi_host',None)


    facets=sddquery.search_api_parameters(facets_group)

    url=build_url(facets,searchapi_host)

    query={}
    query['url']=url
    query['attached_parameters']=sddquery.synchro_data_parameters(facets_group)

    return query

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-',help='Facets groups file')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    facets_groups=sdpipelineutils.get_input_data(args.file)
    queries=run(facets_groups)
    sdprint.print_format(queries,args.format,args.print_only_one_item)
