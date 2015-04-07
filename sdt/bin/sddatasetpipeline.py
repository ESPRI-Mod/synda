#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script runs "dataset" pipeline's jobs."""

import sys
import argparse
import json
import sdapp
import sdconfig
import sdprepare_dataset_attr
import sdshrink
import sdremoveaggregation
import sdcomplete
import sdconst
import sdprint
import sdstatusfilter
from sdexception import SDException

def run(**kw):
    files=kw.get('files')
    check_type(files)
    files=sdremoveaggregation.run(files)
    files=sdprepare_dataset_attr.run(files)
    files=sdshrink.run(files)
    files=sdcomplete.run(files)
    files=sdstatusfilter.run(files)
    return files

def check_type(files):
    for f in files:
        type=f['type']
        if type!=sdconst.SA_TYPE_DATASET:
            raise SDException('SDDAPIPE-001','Incorrect type (%s)'%type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    path=None
    buffer=None
    if args.file == "-":
        files=json.load( sys.stdin )
    else:
        path=sdconfig.find_selection_file(args.file)
        with open(path, 'r') as fh:
            files=json.load( fh )

    files=run(files=files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
