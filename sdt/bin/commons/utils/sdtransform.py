#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains transformation filter."""

import re
from sdt.bin.commons.pipeline import sdpostpipelineutils
from sdt.bin.commons.utils import sdexception


def run(files):
    files = transform_url(files)
    return files


def transform_url(files):
    url_replace = sdpostpipelineutils.get_attached_parameter__global(files, 'url_replace')

    if url_replace is not None:
        (from_string, to_string) = parse_rule('url_replace', url_replace)
        for f in files:
            f['url'] = f['url'].replace(from_string, to_string)

    return files


def parse_rule(name, body):
    match = re.search('^s\|([^|]+)\|([^|]*)\|$', body)
    if match is not None:
        from_string = match.group(1)
        to_string = match.group(2)
    else:
        raise sdexception.SDException("SYNDTRAN-001", "Incorrect format for '{}' parameter ({})".format(name, body))
    return from_string, to_string
