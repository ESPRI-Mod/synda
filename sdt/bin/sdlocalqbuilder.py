#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script build SQL query from facets

Note
    'sdlocalqbuilder' means 'SynDa local query builder'
"""

import re
import os
import sys
import argparse
import json
import sdapp
import sdlog
import sddquery
import sdpipelineutils
import sdproduct
import sdconst
import sddquery
import sdprint
from sdexception import SDException

def run(facets_groups):
    """Builds queries.

    Args:
      facets_groups (list of dict): facets groups
    """
    queries=[]
    for dquery in facets_groups:

        # build limit clause
        if 'limit' in dquery:
            limit=sddquery.get_scalar(dquery,'limit',type_=int)

            if limit==0:
                limit_clause=''
            else:
                limit_clause=' limit %i'%limit 

            del dquery['limit']
        else:
            limit_clause=''

        # build sql query
        type_=sddquery.get_scalar(dquery,'type')
        if type_==sdconst.SA_TYPE_FILE:
            sqlquery=build_file_query(dquery)
        elif type_==sdconst.SA_TYPE_DATASET:
            sqlquery=build_dataset_query(dquery)
        else:
            raise SDException('SDLOQUBU-001','Incorrect type (%s)'%type_)

        # Add limit clause
        sqlquery+=limit_clause

        query={}
        query['sqlquery']=sqlquery
        query['attached_parameters']={'type':dquery['type']}

        queries.append(query)

    return queries

def build_file_query(facets):

    # build where clause
    if 'local_path' in facets:
        # 'local_path' based search

        q="select * from file where %s"%" OR ".join(["local_path like '%%%s%%'"%sdproduct.replace_product_with_sql_wildcard(lp) for lp in facets['local_path']])

    elif 'query' in facets:
        # 'file_functional_id' based free text search using 'like' operator

        value=facets['query'][0] # 'query' is always scalar (space and comma characters can't be used for now in this filter)
        buf="'%%%s%%'"%value
        q="select * from file where file_functional_id like %s order by file_functional_id desc"%(buf,)
    else:
        # mainstream search

        di=dict((k, facets[k]) for k in facets if k in ['insertion_group_id','status','error_msg','sdget_status','data_node','model','project','variable','filename']) # keep only local compatible keys
        if len(di)<1:
            q="SELECT * FROM file"
        else:
            serialized_parameters=serialize_parameters(di)
            q="SELECT * FROM file WHERE {0} ".format(serialized_parameters)

    return q

def build_dataset_query(facets):

    # build where clause
    if 'local_path' in facets:
        # 'local_path' based search

        q="select * from dataset where %s"%" OR ".join(["local_path like '%%%s%%'"%sdproduct.replace_product_with_sql_wildcard(lp) for lp in facets['local_path']])

    elif 'query' in facets:
        # 'dataset_functional_id' based free text search using 'like' operator

        value=facets['query'][0] # 'query' is always scalar (space and comma characters can't be used for now in this filter)
        buf="'%%%s%%'"%value
        q="select * from dataset where dataset_functional_id like %s order by dataset_functional_id desc"%(buf,)
    else:
        # mainstream search

        di=dict((k, facets[k]) for k in facets if k in ['status','model','project']) # keep only local compatible keys
        if len(di)<1:
            q="SELECT * FROM dataset"
        else:
            serialized_parameters=serialize_parameters(di)
            q="SELECT * FROM dataset WHERE {0} ".format(serialized_parameters)

    return q

    # SQL query samples
    #q=select * from file where project='CMIP5' and variable='psl' and model not in ('IPSL-CM5A-LR') and (+file_functional_id like '%rcp45%' or +file_functional_id like '%rcp85%' OR +file_functional_id like '%.historical.%') and status='done' ;
    #q="SELECT * FROM file WHERE project={1} AND variable={2} AND model={3} ".format(serialized_parameters)

def serialize_parameters(facets):
    filters=[]
    for k,v in facets.iteritems():
        filters.append(serialize_parameter(k,v))

    return " AND ".join(filters)

def serialize_parameter(name,values):
    """Serialize one parameter

    Example
        input
            name='variable'
            values=['tasmin','tasmax']
        output
            "variable=tasmin OR variable=tasmax"
    """
    l=[]
    for v in values:
        l.append("%s='%s'"%(name,v))

    if len(l)>0:
        buf=" OR ".join(l)
        return "(%s)"%buf
    else:
        return ""

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
