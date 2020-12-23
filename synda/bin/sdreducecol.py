#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script remove unused columns."""

import sys
import argparse
import json
import sdapp
import sdprint
import sdtools

def run(files):
    files=remove_unused_fields(files)
    files=remove_facets(files)
    return files 

def remove_unused_fields(files):

    li=[ 'index_node'
        ,'instance_id'
        ,'cf_standard_name'
        ,'drs_id'
        ,'format'
        ,'metadata_format'
        ,'variable_long_name'
        ,'variable_units'
        ,'forcing'
        ,'description'
        ,'master_id'
        ,'master_gateway']

    for file in files:
        sdtools.remove_dict_items(file,li)

    return files

def remove_facets(files):
    """
    Note
        - 'variable', 'project' and 'model' facets are kept.
    """
    for file in files:
        for k in [ 'realm'
                  ,'institute'
                  ,'ensemble'
                  ,'cmor_table'
                  ,'product'
                  ,'experiment'
                  ,'time_frequency']:
            try:
                del file[k]
            except KeyError:
                pass
    return files

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    files=run(files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
