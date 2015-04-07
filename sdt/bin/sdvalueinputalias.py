#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module adds aliases for some parameters values (used for transition
period, but to be removed ASAP as it's better have only one way to name values
across selections)."""

import os
import sys
import argparse
import json
import sdapp
from sdtypes import Selection
import sdprint
import sdtranslate

def run(facets_groups):
    for facets_group in facets_groups:
        sdtranslate.translate_value(facets_group,value_rules)
    return facets_groups

value_rules={
    'model': {
		'inmcm4'      :'INM-CM4',
		'bcc-csm1-1'  :'BCC-CSM1-1',
		'bcc-csm1-1-m':'BCC-CSM1-1-m',
		'GFDL-CM2p1'  :'GFDL-CM2-1'
    },
    'institute': {
        'CCCma':'CCCMA'
    }
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )

    facets_groups=run(facets_groups)

    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
