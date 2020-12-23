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
    - Some processing done in this module overlap with sdcheckparam module, but
      most don't, so both module are required.
    - This filter is idempotent (i.e. same result if applied many times)
"""

import sys
import argparse
import json
import sdapp
from sdexception import SDException
import sdconst
import sdparam
import sddquery
import sdidtest
import sdconfig
import sdprint

def run(facets_groups):
    for facets_group in facets_groups:
        type_=sddquery.get_scalar(facets_group,'type',default=sdconst.SA_TYPE_FILE) 

        if sdconst.PENDING_PARAMETER in facets_group:
            pending_parameters=facets_group[sdconst.PENDING_PARAMETER]
            del facets_group[sdconst.PENDING_PARAMETER]

            for pvalue in pending_parameters:

                # HACK: this is to prevent 'SYDPARAM-002' exception when using the following construct 'variable[*]=sic evap' in selection file
                # (TODO: find a better way to handle this hack)
                if pvalue=='*':
                    continue

                pname=infere_parameter_name(pvalue,type_)

                if pname in facets_group:
                    facets_group[pname].append(pvalue)
                else:
                    facets_group[pname]=[pvalue]

    return facets_groups

def infere_parameter_name(pvalue,type_):
    if pvalue.isdigit():
        pname='limit' # deprecated: do no use this anymore
        # pname='query' # replace with this asap

    elif sdidtest.is_url(pvalue):
        pname='url'
    elif sdidtest.is_file_functional_id(pvalue):

        # Use ESGF free text 'query' parameter
        #
        # Beware: this mode is experimental and seems not reliable (see TAG543N45K3KJK for info)
        #
        #pname='query'

        # Use instance_id
        pname='instance_id'

    elif sdidtest.is_filename(pvalue):
        pname='title'
    elif sdidtest.is_dataset_functional_id(pvalue):
        if type_==sdconst.SA_TYPE_FILE:

            if sdconfig.dataset_filter_mecanism_in_file_context=='query':

                # Use ESGF free text 'query' parameter
                #
                # Beware: this mode is experimental and seems not reliable (see TAG543N45K3KJK for info )
                #
                pname='query'

            elif sdconfig.dataset_filter_mecanism_in_file_context=='dataset_id':

                # Use 'dataset_id' parameter with the 'sdcompletedatasetid' filter
                #
                # Beware: this trigger a search-api call in 'sdcompletedatasetid' filter
                #
                pname='dataset_id'

            else:
                raise SDException('SDINFERE-040','Unknown value (%s)'%sdconfig.dataset_filter_mecanism_in_file_context)

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
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
