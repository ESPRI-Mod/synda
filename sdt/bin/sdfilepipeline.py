#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script runs "file" pipeline's jobs.

Usage
 - cat file | sdfilepipeline -
 - cat file | sdfilepipeline
 - sdfilepipeline file
"""

import sys
import argparse
import json
import sdapp
import sdconfig
import sdreducecol
import sdreducerow
import sdtimefilter
import sdprepare_dataset_attr
import sdprepare_file_attr
import sdlocalpath
import sdcheck_dataset_template
import sdremoveaggregation
import sdcomplete
#import sdonemgf_post
import sdshrink
import sdprint
import sdlog
import sdstatusfilter
import sdprotocol
from sdexception import SDException

def run(**kw):
    files=kw.get('files')
    check_type(files)
    check_fields(files)
    files=sdreducerow.run(files)
    files=sdremoveaggregation.run(files)
    files=sdprotocol.run(files)
    files=sdtimefilter.run(files)
    files=sdprepare_dataset_attr.run(files)
    #files=sdcheck_dataset_template.run(files)
    files=sdreducecol.run(files)
    files=sdprepare_file_attr.run(files)
    files=sdlocalpath.run(files)

    for f in files:
        sdlog.debug("SDFIPIPE-004","%s"%f['url'],stdout=True)

    files=sdshrink.run(files)

    for f in files:
        sdlog.debug("SDFIPIPE-005","%s"%f['url'],stdout=True)

    #files=sdonemgf_post.run(files) # BEWARE: this module do not respect 'KISS' principle (it updates global value by altering the sdtc console session context). You can disable it to keep things simple (it's only there for tuning purpose).
    files=sdcomplete.run(files)

    files=sdstatusfilter.run(files)

    return files

def check_type(files):
    for f in files:
        type=f['type']
        if type!='File':
            raise SDException('SDFIPIPE-001','Incorrect type (%s)'%type)

def check_fields(files):
    """This func is to prevent user to set 'fields' attribute (this attribute is set only by the program, in specific cases)."""

    for f in files:
        if 'fields' in f:
            raise SDException('SDFIPIPE-002',"'fields' parameter can't be used in 'file' pipeline (fields=%s)"%f['fields'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-')
    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='raw')
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
