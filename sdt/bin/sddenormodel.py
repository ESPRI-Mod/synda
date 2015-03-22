#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sddenormodel.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Denormalize model names as search-API don't understand normalized model name."""

import sys
import argparse
import json
import sdapp
import sdparam
import sdprint

def run(facets_groups):
    facets_groups_new=[]

    for facets_group in facets_groups:
        facets_group=denormalize_models(facets_group)
        facets_groups_new.append(facets_group)

    return facets_groups_new

def denormalize_models(facets_group):
    if 'model' in facets_group:
        facets_group['model']=sdparam.denormalize_models_list(facets_group['model'])

    return facets_group

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
