#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains inference routines.

Notes
    - This module resolve pending parameters
    - This module uses 'duck typing' method for facet inference
    - This module inferes everything but the type.
      We don't infere the type here because we need the type to resolve some
      special case (e.g. because of search-API complex naming rules, we
      sometimes want the dataset_functional_id to resolve into 'query' and
      sometimes into 'instance_id'). 
      If want to infere the type (i.e. infere type from id instead of id from
      type), use syndautils.infer_type() func.
"""

import sys
import argparse
import json
import sdapp
from sdexception import SDException
import sdconst
import sdparam
import sdi18n
import sddquery
import sdidtest
import sdconfig
import sdprint

def run(facets_groups):
    for facets_group in facets_groups:
        type_=sddquery.get_scalar(facets_group,'type',default=sdconst.SD_TYPE_DEFAULT) 

        if sdconst.PENDING_PARAMETER in facets_group:
            pending_parameters=facets_group[sdconst.PENDING_PARAMETER]
            del facets_group[sdconst.PENDING_PARAMETER]

            for pvalue in pending_parameters:
                pname=infere_parameter_name(pvalue,type_)

                if pname in facets_group:
                    facets_group[pname].append(pvalue)
                else:
                    facets_group[pname]=[pvalue]

    return facets_groups

def infere_parameter_name(pvalue,type_):
    if pvalue.isdigit():
        pname='limit'
    elif sdidtest.is_file_functional_id(pvalue):
        pname='query'
    elif sdidtest.is_filename(pvalue):
        pname='title'
    elif sdidtest.is_dataset_functional_id(pvalue):
        if type_==sdconst.SA_TYPE_FILE:
            pname='query' # new behaviour (previously, we were using dataset_id here, with the 'sdcompletedatasetid' filter)
        elif type_==sdconst.SA_TYPE_DATASET:
            pname='instance_id'
        else:
            raise SDException('SDINFERE-001','Unknown type (%s)'%type_)
    elif sdidtest.is_dataset_local_path(pvalue):
        pname='local_path'
    elif sdidtest.is_file_local_path(pvalue):
        pname='local_path'
    else:
        try:
            pname=sdparam.get_name_from_value(pvalue)
        except SDException,e:
            if sdconfig.config.getint('behaviour','check_parameter')==1:
                raise
            else:
                pname='query' # fallback to free pattern

    return pname

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
