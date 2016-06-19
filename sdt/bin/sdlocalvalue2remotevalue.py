#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module translates facets local value to remote value.

Notes
    - This filter run before the search-api call.
    - 'url' in this module has nothing to do with 'url' in sdremoteqbuilder module
"""

import sys
import argparse
import json
import sdapp
import sdprint
import sdutils
import sdconst

def local_urls_to_remote_urls(local_urls):
    remote_urls=[]

    for local_url in local_urls:

        protocol=sdutils.get_transfer_protocol(local_url)

        gridftp_suffix='|application/gridftp|GridFTP'
        opendap_suffix='|application/opendap-html|OPENDAP'
        http_suffix='|application/netcdf|HTTPServer'

        if protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:
            suffix=gridftp_suffix
        elif protocol==sdconst.TRANSFER_PROTOCOL_OPENDAP:
            suffix=opendap_suffix
        elif protocol==sdconst.TRANSFER_PROTOCOL_HTTP:
            suffix=http_suffix
        else:
            suffix=http_suffix # if unknown, default to HTTP

        remote_url='%s%s'%(local_url,suffix)
        remote_urls.append(remote_url)

    return remote_urls

def run(facets_groups):
    for facets_group in facets_groups:

        if 'url' in facets_group:

            urls=facets_group['url'] # memo: facet in facets_group are array

            facets_group['url']=local_urls_to_remote_urls(urls)

    return facets_groups

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
