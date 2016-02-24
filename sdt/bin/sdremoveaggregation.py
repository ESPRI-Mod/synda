#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script remove aggregation."""

import sys
import argparse
import sdconst
import json
import sdapp
import sdprint
from sdexception import SDException

def run(files):
    files=remove_aggregation(files)
    return files 

def remove_aggregation(files):
    files_without_aggregation=[]
    for f in files:
        if is_aggregation(f):
            pass
        else:
            files_without_aggregation.append(f)
    return files_without_aggregation

def is_aggregation(f):
    if f["type"]==sdconst.SA_TYPE_FILE:

        # sample aggregation file
        #  cmip5.output1.BCC.bcc-csm1-1-m.rcp26.day.atmos.day.r1i1p1.clt.20120910.aggregation

        result=('.aggregation' in f.get("title"))

    elif f["type"]==sdconst.SA_TYPE_DATASET:

        # sample aggregation dataset
        #  obs4MIPs.LOA_IPSL.PARASOL.day.parasolRefl.1.aggregation.8

        result=('.aggregation.' in f.get("instance_id"))

    else:
        raise SDException('SDRMAGGR-001','Incorrect type (%s)'%f["type"])

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
