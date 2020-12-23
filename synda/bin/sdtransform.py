#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains transformation filter."""

import sys
import argparse
import json
import re
import sdapp
import sdprint
import sdpostpipelineutils
import sdexception

def run(files):
    files=transform_url(files)
    return files

def transform_url(files):

    url_replace=sdpostpipelineutils.get_attached_parameter__global(files,'url_replace')

    if url_replace is not None:
        (from_string,to_string)=parse_rule('url_replace',url_replace)
        for f in files:
            f['url']=f['url'].replace(from_string,to_string)

    return files

def parse_rule(name,body):
    match=re.search('^s\|([^|]+)\|([^|]*)\|$',body)
    if match!=None:
        from_string=match.group(1)
        to_string=match.group(2)
    else:
        raise sdexception.SDException("SYNDTRAN-001","Incorrect format for '%s' parameter (%s)"%(name,body))

    return (from_string,to_string)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
