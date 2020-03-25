#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module removes file duplicates and replica.

Notes
    - This module removes duplicate files in a random way (i.e. all files have the same chance to be removed).
    - This module removes replicates
    - sdrmdup means 'SynDa ReMove DUPlicate and REPlicate'

See also
    - sdshrink
"""

from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.facets import sdlmattrfilter
from sdt.bin.commons.pipeline import sdpipelineprocessing


def run(metadata, functional_id_keyname):
    sdlog.info("SYNDRMDR-001", "Build 'seen' table..")
    # create light list with needed columns only not to overload system memory
    light_metadata = sdlmattrfilter.run(metadata, [functional_id_keyname])
    # build 'seen' data structure (list of dict => dict (id=>bool))
    seen = dict((f[functional_id_keyname], False) for f in light_metadata.get_files())  # warning: load list in memory

    sdlog.info("SYNDRMDR-002", "Perform duplicate and replicate suppression..")

    po = sdpipelineprocessing.ProcessingObject(remove, functional_id_keyname, seen)
    metadata = sdpipelineprocessing.run_pipeline(metadata, po)

    return metadata


def remove(files, functional_id_keyname, seen):
    new_files = []
    for f in files:
        uniq_id = f[functional_id_keyname]
        if not seen[uniq_id]:
            new_files.append(f)
            seen[uniq_id] = True  # mark as seen so other duplicate will be excluded (first item in the loop win)
    return new_files
