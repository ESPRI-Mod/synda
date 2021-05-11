#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.sdt import sdapp
from synda.sdt import sdprint
from synda.sdt import sdtools
from synda.sdt import sdlog
from synda.sdt.sdexception import SDException
from synda.sdt import sdpostpipelineutils

from synda.source.config.process.download.constants import get_transfer_protocol


def run(files):

    for _file in files:
        protocol = \
            sdpostpipelineutils.get_attached_parameter(
                _file,
                'protocol',
                default=get_transfer_protocol(),
            )

        if protocol == get_transfer_protocol():
            if 'url_http' in _file:
                _file['url'] = _file['url_http']
            elif 'url_gridftp' in _file:
                sdlog.warning(
                    'SYNPROTO-001',
                    'Fallback to gridftp as http url is missing',
                )
                _file['url'] = _file['url_gridftp']

        else:
            raise SDException(
                "SYNPROTO-004",
                "Incorrect protocol (%s)" % protocol,
            )

        sdtools.remove_dict_items(
            _file,
            ['url_gridftp', 'url_http'],
        )

    return files


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1', '--print_only_one_item', action='store_true')
    parser.add_argument('-F', '--format', choices=sdprint.formats, default='raw')
    args = parser.parse_args()

    files_ = json.load(sys.stdin)
    files_ = run(files_)
    sdprint.print_format(
        files_,
        args.format,
        args.print_only_one_item,
    )
