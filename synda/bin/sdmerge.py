#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script merges json chunks into one json document.

Note
    This script is intended to process 'sdprint.print_format' output
    in 'raw' mode or 'line' mode (not 'indent' mode)
"""

import sys
import argparse
import json
import sdprint

def run(lines):
    files=[]

    for l in lines:

        if l.startswith('['):
            # many file dicts by line

            items=json.loads( l )
            files.extend(items)

        elif l.startswith('{'):
            # one file dict by line

            item=json.loads( l )
            files.append(item)
        else:
            assert False

    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    lines=sys.stdin.readlines()
    files=run(lines)
    sdprint.print_format(files,args.format)
