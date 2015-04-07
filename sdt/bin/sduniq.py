#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module removes file duplicates (e.g. replica).

Notes
    - This module  removes duplicate files in a random way (i.e. all files have the same chance to be removed).
    - This module deals with two types of duplicates (see comments in sdshrink for details).
"""

import sdapp
import sdconst
import sdprint
import sdpostpipelineutils

def run(files,keep_replica=False):
    files=remove_duplicate(files,keep_replica)
    return files

def remove_duplicate(files,keep_replica):
    """This func remove uniq_id duplicates."""

    files_without_duplicate={}
    for f in files:

        if keep_replica:
            uniq_id=(sdpostpipelineutils.get_functional_identifier_value(f),f['data_node'])
        else:
            uniq_id=sdpostpipelineutils.get_functional_identifier_value(f)

        files_without_duplicate[uniq_id]=f # duplicates are removed here (last item in the loop win)

    return files_without_duplicate.values()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
