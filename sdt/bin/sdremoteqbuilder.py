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

def build_query(facets_group):
    query={}

    assert(isinstance(facets_group,dict))


    # set default type
    if 'type' not in facets_group:
        facets_group['type']=['File'] # set as list (all Search-API facets are list at this point)

    # if 'fields' not set, we retrieve all attributes
    if 'fields' not in facets_group:
        facets_group['fields']=['*']


    searchapi_host=facets_group.get('searchapi_host',None)
    action=facets_group.get('action',None)


    facets=sddquery.search_api_parameters(facets_group)


    query['url']=sdremotequtils.build_url(facets,searchapi_host)

    query['attached_parameters']=sddquery.synchro_data_parameters(facets_group)



    # hack to retrieve datasets timestamps in one row
    if action is not None:
        if action=='install':

            # force attributes for dataset timestamp retrieval
            facets['type']=['Dataset']
            facets['fields']=['timestamp','_timestamp','instance_id'] # we also add '_timestamp' as some project use this naming (e.g.ahttp://esgf-index1.ceda.ac.uk/esg-search/search?fields=timestamp,_timestamp&instance_id=cordex.output.EUR-11.DHMZ.ECMWF-ERAINT.evaluation.r1i1p1.RegCM4-2.v1.day.ps.v20150527). Note that search-API 'fields' attribute can contains non-existent fields (i.e. no error occurs in such case, fields are just ignored)

            query['dataset_timestamp_url']=sdremotequtils.build_url(facets,searchapi_host)



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
