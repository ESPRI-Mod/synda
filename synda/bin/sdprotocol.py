#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module selects which protocol to use depending on configuration."""

import sys
import argparse
import json
import sdapp
import sdconst
import sdprint
import sdtools
import sdlog
from sdexception import SDException
import sdpostpipelineutils

def run(files):
    for file in files:
        protocol=sdpostpipelineutils.get_attached_parameter(file,'protocol',sdconst.TRANSFER_PROTOCOL_HTTP)

        if protocol not in sdconst.TRANSFER_PROTOCOLS:
            raise SDException("SYNPROTO-004","Incorrect protocol (%s)"%protocol)

        if protocol == sdconst.TRANSFER_PROTOCOL_GLOBUS:
            if 'url_globus' in file:
                file['url'] = file['url_globus']
            elif 'url_gridftp' in file:
                file['url'] = file['url_gridftp']
            elif 'url_http' in file:
                sdlog.warning('SYNPROTO-005','Fallback to http as globus url is missing')
                file['url'] = file['url_http']

        elif protocol == sdconst.TRANSFER_PROTOCOL_GRIDFTP:
            if 'url_gridftp' in file:
                file['url'] = file['url_gridftp']
            elif 'url_http' in file:
                sdlog.debug('SYNPROTO-002','Fallback to http as gridftp url is missing (%s)'%file["title"])
                file['url'] = file['url_http']

        elif protocol == sdconst.TRANSFER_PROTOCOL_HTTP:
            if 'url_http' in file:
                file['url'] = file['url_http']
            elif 'url_gridftp' in file:
                sdlog.warning('SYNPROTO-001','Fallback to gridftp as http url is missing')
                file['url'] = file['url_gridftp']

        else:
            raise SDException("SYNPROTO-003","Incorrect protocol (%s)"%protocol)

        sdtools.remove_dict_items(file,['url_globus', 'url_gridftp', 'url_http', 'url_opendap'])

    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
