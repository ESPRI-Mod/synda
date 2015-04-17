#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module selects which protocol to use depending on configuration."""

import sys
import argparse
import json
import sdapp
import sdconst
import sdprint
import sdtools
import sdpostpipelineutils

def run(files):
    for file in files:
        protocol=sdpostpipelineutils.get_attached_parameter(file,'protocol',sdconst.TRANSFER_PROTOCOL_HTTP)


        if protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP and 'url_gridftp' in file:
            file['url']=file['url_gridftp']
        elif protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP and 'url_gridftp' not in file:
            file['url']=file['url_http'] # fallback
        elif protocol==sdconst.TRANSFER_PROTOCOL_HTTP and 'url_http' in file:
            file['url']=file['url_http']
        elif protocol==sdconst.TRANSFER_PROTOCOL_HTTP and 'url_http' not in file:
            assert False # if happens, should have been removed by sdreducerow

        sdtools.remove_dict_items(file,['url_gridftp', 'url_http'])

    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
