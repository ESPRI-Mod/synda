#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains generic printing routines."""

import json
import sys
import argparse

def print_format(files,format,print_only_one_item=False,fh=sys.stdout):
    """Print files list with given format."""

    if print_only_one_item:
        files=[files[0]]
        format='indent' # force format to indent when displaying only one item

    if format == 'raw':
        fh.write("%s\n"%json.dumps(files))
    elif format == 'line':
        for f in files:
            fh.write("%s\n"%json.dumps(f))
    elif format == 'indent':
        fh.write("%s\n"%json.dumps(files,indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='indent')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    print_format(files,args.format)
