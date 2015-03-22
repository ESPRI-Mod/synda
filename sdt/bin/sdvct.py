#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdvct.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module is a plugin to handle Synchro-data "varname:cmor_tblname" syntax.

Note
    sdvct means "Synchro-Data Varname:Cmor_Tblname"
"""

import sys
import argparse
import json
import copy
import sdapp
import sdprint

def run(facets_groups):
    new_facets_groups=[]
    for facets_group in facets_groups:
        if "variable" in facets_group:

            variables_with_cmortable=[]
            variables_without_cmortable=[]

            for v in facets_group['variable']:
                if ":" in v:
                    variables_with_cmortable.append(v)
                else:
                    variables_without_cmortable.append(v)

            del facets_group['variable']

            # create new query for each variable with cmortable
            for v in variables_with_cmortable:
                (varname,cmor_table)=v.split(':')
                f_cpy=copy.deepcopy(facets_group)

                f_cpy['variable']=[varname]
                f_cpy['cmor_table']=[cmor_table]

                new_facets_groups.append(f_cpy)

            # create one more query for all variable without cmortable
            if len(variables_without_cmortable)>0:

                f_cpy=copy.deepcopy(facets_group)
                f_cpy['variable']=variables_without_cmortable

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
