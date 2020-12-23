#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module replace special chars (in values only as keys do not contain special chars).

Note
    The primary raison for this filter is to decode encoded space in selection file (e.g. project="ISI-MIP%20Fasttrack").
"""

import sys
import argparse
import json
import sdapp
import sdconst
import sddquery
import sdprint

def run(facets_groups):
    facets_groups_new=[]

    for facets_group in facets_groups:
        facets_group=decode_special_chars(facets_group)
        facets_groups_new.append(facets_group)

    return facets_groups_new

def decode_special_chars(facets_group):
    for k in sddquery.search_api_parameters(facets_group).keys():
        facets_group[k]=decode_values(facets_group[k])

    return facets_group

def decode_values(values):
    new_values=[]

    for v in values:
        new_values.append(v.replace('%20',' '))

    return new_values

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
