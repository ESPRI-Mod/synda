#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module dumps data in bulk mode.

Example of use
    sddump.py CMIP5 atmos searchapi_host=esgf-data.dkrz.de -f timestamp
"""

from sdt.bin.commons.search import sdsearch
from sdt.bin.commons.param import sddeferredafter
from sdt.bin.commons.search import sdstreamutils


def dump_ESGF(parameter=None, selection_file=None, fields=None, dry_run=False, playback=None, record=None,
              no_default=True, type_='Dataset'):
    """This func dumps fields for all ESGF matching files/datasets.

    Initially designed to batch update attribute in Synda database
    (e.g. when a new attribute is decided to be stored in Synda,
    all already downloaded files metadata must be updated).
    """
    stream = sdstreamutils.get_stream(parameter=parameter, selection_file=selection_file, no_default=no_default)

    sddeferredafter.add_forced_parameter(stream, 'replica', 'false')

    sddeferredafter.add_forced_parameter(stream, 'type', type_)

    assert fields is not None
    sddeferredafter.add_forced_parameter(stream, 'fields', fields)

    metadata = sdsearch.run(stream=stream, post_pipeline_mode=None, dry_run=dry_run, playback=playback, record=record)
    return metadata.get_files()
