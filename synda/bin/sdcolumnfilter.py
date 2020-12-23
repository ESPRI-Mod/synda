#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module filters a columns list."""

import sys
import argparse
import json
import sdprint

def run(files,key_list_to_keep):

    if len(key_list_to_keep)==0:
        return files
    else:
        new_list=[]

        for f in files:
            new_list.append(dict((k, f[k]) for k in f if k in key_list_to_keep))

        return new_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-C','--column',type=lambda s: s.split(','),default=[],help="set column(s) to keep")
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files,args.column)
    sdprint.print_format(files,args.format)
