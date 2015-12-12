#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Fix incorrect case for parameter value.

Example
    cmip5 (incorrect case) is transformed into CMIP5
"""

import sys
import argparse
import json
import sdapp
from sdexception import SDException
import sdconst
import sdparam
import sdidtest
import sdconfig
import sdprint

def run(facets_groups):
    for facets_group in facets_groups:
        if sdconst.PENDING_PARAMETER in facets_group:
            new_pending_parameter=[]
            for pvalue in facets_group[sdconst.PENDING_PARAMETER]:

                # HACK: this is to prevent 'SYDPARAM-002' exception when using the following construct 'variable[*]=sic evap' in selection file
                if pvalue=='*':
                    continue

                fixed_pvalue=fix_case(pvalue)
                new_pending_parameter.append(pvalue)

            del facets_group[sdconst.PENDING_PARAMETER]

    return facets_groups

def fix_case(pvalue):
    if pvalue.isdigit():
        pass
    elif sdidtest.is_file_functional_id(pvalue):
        pass
    elif sdidtest.is_filename(pvalue):
        pass
    elif sdidtest.is_dataset_functional_id(pvalue):
        pass
    elif sdidtest.is_dataset_local_path(pvalue):
        pass
    elif sdidtest.is_file_local_path(pvalue):
        pass
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
