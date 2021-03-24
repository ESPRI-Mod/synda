#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.sdt import sdapp
from synda.sdt import sdprint
from synda.sdt import sdutils

from synda.source.config.process.download.constants import get_transfer_protocols

def local_urls_to_remote_urls(local_urls):

    remote_urls = []

    for local_url in local_urls:

        protocol = sdutils.get_transfer_protocol(local_url)

        gridftp_suffix = '|application/gridftp|GridFTP'
        http_suffix = '|application/netcdf|HTTPServer'

        if protocol == get_transfer_protocols()['gridftp']:
            suffix = gridftp_suffix
        elif protocol == get_transfer_protocols()['http']:
            suffix = http_suffix
        else:
            # if unknown, default to HTTP
            suffix = http_suffix

        remote_url = '%s%s' % (local_url, suffix)
        remote_urls.append(remote_url)

    return remote_urls


def run(facets_groups):

    for facets_group in facets_groups:

        if 'url' in facets_group:
            # memo: facet in facets_group are array
            urls = facets_group['url']

            facets_group['url'] = local_urls_to_remote_urls(urls)

    return facets_groups


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1', '--print_only_one_item', action='store_true')
    parser.add_argument('-F', '--format', choices=sdprint.formats, default='raw')
    args = parser.parse_args()

    facets_groups_ = json.load(sys.stdin)
    facets_groups_ = run(facets_groups_)
    sdprint.print_format(
        facets_groups_,
        args.format,
        args.print_only_one_item,
    )
