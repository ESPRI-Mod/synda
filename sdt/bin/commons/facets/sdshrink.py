#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module reduces the number of files.

Description
    Depending on the context, this filter can do two things:

    Type-A removal: replica instance

        Keep only one instance of each replica. This is needed, because
        in some case (for example with an incorrectly set selection containing
        "variable[*][*]=tas" and "variable[atmos][day]=tas tasmin"), a selection
        can return many copies of the same file).

    Type-B removal: replica

        Keeps only one replica for each file.

Notes
  - This module deals with functional aspects while 'sdreducerow' module deals
    with more technical aspects.
  - This module can be used to process different metadata types (File and Dataset).
"""

from sdt.bin.commons.esgf import sdnearestpost
from sdt.bin.commons.utils import sdlog

from sdt.bin.commons.facets import sdshrinktest
from sdt.bin.commons.facets import sdshrinkutils


def run(metadata):
    # for f in metadata.get_files(): # warning: load list in memory
    #    sdlog.debug("SDSHRINK-004","%s"%f['data_node'],stdout=True)

    metadata = shrink(metadata)

    # for f in metadata.get_files(): # warning: load list in memory
    #    sdlog.debug("SDSHRINK-005","%s"%f['data_node'],stdout=True)

    return metadata


def shrink(metadata):
    if sdshrinktest.is_nearestpost_enabled(metadata):
        # In this case, we remove duplicates by keeping the nearest

        sdlog.info("SDSHRINK-001", "Start nearestpost filter..")
        metadata = sdnearestpost.run(metadata)
        sdlog.info("SDSHRINK-002", "nearestpost filter completed")
    else:
        # In this case, we remove duplicates by using a 'uniq' filter

        sdlog.info("SDSHRINK-008", "Start uniq filter..")
        metadata = sdshrinkutils.uniq(metadata)
        sdlog.info("SDSHRINK-010", "uniq filter completed")

    return metadata
