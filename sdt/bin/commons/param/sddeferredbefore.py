#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This filter is used to process deferred parameters *before* inference.

The reason for this module is we don't want to parse/modify 'parameter' buffer
as it's a complex task to do and as it's already done in 'sdparse' and
'sdinference' module. So we decided to add a mecanism to pass forced/default
values down the pipeline.

Note
    'sddeferredbefore' and 'sddeferredafter' do the same job except one take place
    before inference and the other take place after inference.
"""

from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.search import sdstream
from sdt.bin.commons.param import sddefaultparameter
from sdt.bin.commons.param import sdforcedparameter


def run(facets_groups):
    sddefaultparameter.parameter_name_prefix = sdconst.BIDPP
    facets_groups = sddefaultparameter.run(facets_groups)

    sdforcedparameter.parameter_name_prefix = sdconst.BIFPP
    facets_groups = sdforcedparameter.run(facets_groups)

    return facets_groups


def add_default_parameter(o, name, value):
    if sdstream.is_stream(o):

        # force list if not already
        if not isinstance(value, list):
            value = [value]

        # force str
        value = [str(v) for v in value]

        k = "{}{}".format(sdconst.BIDPP, name)
        for facets_group in o:
            facets_group[k] = value
    else:
        # assume parameter

        o.append("{}{}={}".format(sdconst.BIDPP, name, value))


def add_forced_parameter(o, name, value):
    if sdstream.is_stream(o):

        # force list if not already
        if not isinstance(value, list):
            value = [value]

        # force str
        value = [str(v) for v in value]

        k = "{}{}".format(sdconst.BIFPP, name)
        for facets_group in o:
            facets_group[k] = value
    else:
        # assume parameter

        o.append("{}{}={}".format(sdconst.BIFPP, name, value))
