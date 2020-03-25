#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module selects which protocol to use depending on configuration."""

from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdtools
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils.sdexception import SDException
from sdt.bin.commons.pipeline import sdpostpipelineutils


def run(files):
    for file in files:
        protocol = sdpostpipelineutils.get_attached_parameter(file, 'protocol', sdconst.TRANSFER_PROTOCOL_HTTP)

        if protocol not in sdconst.TRANSFER_PROTOCOLS:
            raise SDException("SYNPROTO-004", "Incorrect protocol ({})".format(protocol))

        if 'url_gridftp' in file and 'url_http' in file:

            if protocol == sdconst.TRANSFER_PROTOCOL_GRIDFTP:
                file['url'] = file['url_gridftp']
            elif protocol == sdconst.TRANSFER_PROTOCOL_HTTP:
                file['url'] = file['url_http']
            else:
                raise SDException("SYNPROTO-003", "Incorrect protocol ({})".format(protocol))

        elif 'url_gridftp' in file:
            # only gridftp

            if protocol == sdconst.TRANSFER_PROTOCOL_HTTP:
                sdlog.warning('SYNPROTO-001', 'Fallback to gridftp as http url is missing')

            file['url'] = file['url_gridftp']

        elif 'url_http' in file:
            # only http

            if protocol == sdconst.TRANSFER_PROTOCOL_GRIDFTP:
                sdlog.debug('SYNPROTO-002', 'Fallback to http as gridftp url is missing ({})'.format(file["title"]))

            file['url'] = file['url_http']

        else:
            # no url available to download the file
            # (should not be here as sdremoverow takes care of those cases)

            assert False
        sdtools.remove_dict_items(file, ['url_gridftp', 'url_http', 'url_opendap'])

    return files
