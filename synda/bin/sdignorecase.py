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

    # if filter not enabled in config file, leave without doing anything
    if sdconfig.config.getboolean('behaviour','ignorecase') == False:
        return facets_groups

    for facets_group in facets_groups:
        if sdconst.PENDING_PARAMETER in facets_group:
            new_pending_parameter=[]


            for pvalue in facets_group[sdconst.PENDING_PARAMETER]:

                # HACK: this is to prevent 'SYDPARAM-002' exception when using the following construct 'variable[*]=sic evap' in selection file
                # (TODO: find a beter way to handle this hack)
                if pvalue=='*':
                    continue

                if is_case_incorrect(pvalue):
                    fixed_value=sdparam.fix_value_case(pvalue)
                    new_pending_parameter.append(fixed_value)
                else:
                    new_pending_parameter.append(pvalue)


            facets_group[sdconst.PENDING_PARAMETER]=new_pending_parameter # overwrite previous value

    return facets_groups

def is_case_incorrect(pvalue):
    if pvalue.isdigit():
        return False
    elif sdidtest.is_file_functional_id(pvalue):
        return False
    elif sdidtest.is_filename(pvalue):
        return False
    elif sdidtest.is_dataset_functional_id(pvalue):
        return False
    elif sdidtest.is_dataset_local_path(pvalue):
        return False
    elif sdidtest.is_file_local_path(pvalue):
        return False
    else:
        if sdparam.is_case_incorrect(pvalue):
            return True
        else:
            return False

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
