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

Notes
    - 'sdremoteqbuilder' means 'SynDa remote Query builder'
    - 'url' in this module has nothing to do with 'url' in sdlocalvalue2remotevalue module

Reference
    - https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API
"""

import argparse
import copy
import sdapp
import sdconst
import sdlog
import sddquery
import sdpipelineutils
import sdremotequtils
import sdconfig
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


    # attached_parameters mngt

    query['attached_parameters']=sddquery.synda_parameters(facets_group)



    # hack to retrieve datasets timestamps in one row
    if action is not None:
        if action=='install':
            ds_timstap_facets=transform_facets_for_dataset_timestamp_retrieval(facets)
            query['dataset_timestamp_url']=sdremotequtils.build_url(ds_timstap_facets,searchapi_host) # TAG3JKWW93K4J4JKDZS


    # hack to retrieve datasets attrs in one row
    if sdconfig.copy_ds_attrs:
        if action is not None:
            if action=='install':
                ds_attrs_facets=transform_facets_for_dataset_attrs_retrieval(facets)
                query['dataset_attrs_url']=sdremotequtils.build_url(ds_attrs_facets,searchapi_host) # TAG3JKWW93K4J4JKDZS



    return query

def transform_facets_for_dataset_timestamp_retrieval(facets):
    """Force attributes for dataset timestamp retrieval."""

    # do not alter original facets object
    facets_cpy=copy.deepcopy(facets)

    facets_cpy['type']=['Dataset']


    # to/from facet do not apply here
    #
    # i.e. to/from only apply for to main query.
    #
    # here we want to fill the file dataset timestamp with the corresponding
    # dataset timestamp even if the dataset timestamp is outside of the
    # 'to/from' window
    #
    # this issue happens because the file timestamp may differ from the
    # corresponding dataset timestamp.
    #
    # e.g. cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.v20120928
    #      https://esgf-data.dkrz.de/esg-search/search?cmor_table=Amon&product=output1&realm=atmos&institute=MOHC&fields=dataset_id,id,timestamp&project=CMIP5&to=2015-11-01T01:00:00Z&time_frequency=mon&experiment=rcp85&distrib=true&model=HadGEM2-ES&type=File&ensemble=r1i1p1&format=application%2Fsolr%2Bjson&limit=9000&offset=0
    #      https://esgf-data.dkrz.de/esg-search/search?project=CMIP5&product=output1&realm=atmos&institute=MOHC&fields=instance_id,timestamp,_timestamp,type,size&cmor_table=Amon&time_frequency=mon&experiment=rcp85&distrib=true&model=HadGEM2-ES&type=Dataset&ensemble=r1i1p1&format=application%2Fsolr%2Bjson&limit=9000&offset=0&replica=false
    #
    if 'to' in facets_cpy:
        del facets_cpy['to']
    if 'from' in facets_cpy:
        del facets_cpy['from']


    # we also add '_timestamp' as some project use this naming
    # (e.g.ahttp://esgf-index1.ceda.ac.uk/esg-search/search?fields=timestamp,_timestamp&instance_id=cordex.output.EUR-11.DHMZ.ECMWF-ERAINT.evaluation.r1i1p1.RegCM4-2.v1.day.ps.v20150527).
    # Note that search-API 'fields' attribute can contains non-existent fields
    # (i.e. no error occurs in such case, non-existent fields are just ignored)
    facets_cpy['fields']=sdconst.TIMESTAMP_FIELDS

    return facets_cpy

def transform_facets_for_dataset_attrs_retrieval(facets):
    """Force attributes for dataset attrs retrieval."""

    # do not alter original facets object
    facets_cpy=copy.deepcopy(facets)

    facets_cpy['type']=['Dataset']
    facets_cpy['fields']=['*']

    return facets_cpy

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-',help='Facets groups file')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    facets_groups=sdpipelineutils.get_input_data(args.file)
    queries=run(facets_groups)
    sdprint.print_format(queries,args.format,args.print_only_one_item)
