#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script merges json chunks into one json document.

Note
    This script is intended to process 'sdprint.print_format' output
    in 'raw' mode or 'line' mode (not 'indent' mode)
"""

import argparse
import json
import sdprint

def run(lines):
    files=[]

    for l in lines:

        if l.startswith('['):
            # many file dicts by line

            items=json.load( l )
            files.extend(items)

        elif l.startswith('{'):
            # one file dict by line

            item=json.load( l )
            files.append(item)
        else:
            assert False

    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    lines=sys.stdin.readlines()
    files=run(lines)
    sdprint.print_format(files,args.format)
