#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdlocal2remote.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module translates facets names.

Note
    - this module is not exactly the reverse of the 'sdremote2local' module,
      (e.g. non injective because of 'time_frequency' and 'instance_id')
"""

import sys
import argparse
import json
import sdapp
import sdtranslate
import sdprint

name_rules={
    'frequency' :'time_frequency',
    'filename' :'title',
    'file_functional_id' :'instance_id',
    'dataset_functional_id' :'dataset_id'
}

def run(facets_groups):
    facets_groups_new=[]

    for facets_group in facets_groups:
        facets_group=sdtranslate.translate_name(facets_group,name_rules)
        facets_groups_new.append(facets_group)

    return facets_groups_new

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
