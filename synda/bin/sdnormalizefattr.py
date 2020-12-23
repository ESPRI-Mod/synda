#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains file normalization filter.

Note
    'sdnormalizefattr' means 'SynDa NORMALIZE File ATTRibute'
"""

import sys
import json
import argparse
import sdapp
import sdnormalize
import sdprint

def run(files):
    for f in files:
        if 'checksum_type' in f:
            f['checksum_type']=sdnormalize.normalize_checksum_type(f['checksum_type'])
    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
