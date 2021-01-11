#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This filter is used to process deferred parameters *after* inference.

The reason for this module is we don't want to parse/modify 'parameter' buffer
as it's a complex task to do and as it's already done in 'sdparse' and
'sdinference' module. So we decided to add a mecanism to pass forced/default
values down the pipeline.

Note
    'sddeferredbefore' and 'sddeferredafter' do the same job except one take place
    before inference and the other take place after inference.
"""

import sys
import argparse
import json
import sddefaultparameter
import sdforcedparameter
import sdstream
import sdprint

from synda.source.config.file.selection.constants import AIDPP
from synda.source.config.file.selection.constants import AIFPP


def run(facets_groups):
    sddefaultparameter.parameter_name_prefix = AIDPP
    facets_groups = sddefaultparameter.run(facets_groups)

    sdforcedparameter.parameter_name_prefix = AIFPP
    facets_groups = sdforcedparameter.run(facets_groups)

    return facets_groups


def add_default_parameter(o, name, value):
    if sdstream.is_stream(o):

        # force list if not already
        if not isinstance(value, list):
            value = [value]

        # force str
        value = [str(v) for v in value]

        k = "%s%s" % (AIDPP, name)
        for facets_group in o:
            facets_group[k] = value
    else:
        # assume parameter

        o.append("%s%s=%s" % (AIDPP, name, value))


def add_forced_parameter(o, name, value):
    if sdstream.is_stream(o):

        # force list if not already
        if not isinstance(value, list):
            value = [value]

        # force str
        value = [str(v) for v in value]

        k = "%s%s" % (AIFPP, name)
        for facets_group in o:
            facets_group[k] = value
    else:
        # assume parameter

        o.append("%s%s=%s" % (AIFPP, name, value))


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
