#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdexplode.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module split one query with many values into many queries with one value (for a given facet).

Note
    It is used for example with the 'model' to limit search-API query walltime by having each query dedicated to only one model.

Args
    facets_groups

Returns
    facets_groups
"""

import sys
import argparse
import json
import copy
import sdapp
from sdtypes import File
import sdprint

def run(facets_groups,facet_to_explode='model'):
    new_facets_groups=[]
    for facets_group in facets_groups:
        if facet_to_explode in facets_group:
            facet_to_explode_values=facets_group[facet_to_explode]
            del facets_group[facet_to_explode]

            # create new query for each value
            for value in facet_to_explode_values:
                f_cpy=copy.deepcopy(facets_group)
                f_cpy[facet_to_explode]=[value]
                new_facets_groups.append(f_cpy)

        else:
            new_facets_groups.append(facets_group)
                
    return new_facets_groups

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load(sys.stdin)

    facets_groups=run(facets_groups)

    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
