#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module removes file duplicates.

Notes
    - This module removes duplicate files in a random way (i.e. all files have the same chance to be removed).
    - This module keeps replicates
    - sdrmdup means 'SynDa ReMove DUPlicate'

See also
    - sdshrink
"""

from sdt.bin.commons.facets import sdlmattrfilter
from sdt.bin.commons.pipeline import sdpipelineprocessing


def run(metadata, functional_id_keyname):
    # create light list with needed columns only not to overload system memory
    light_metadata = sdlmattrfilter.run(metadata, [functional_id_keyname, 'data_node'])
    # list of dict => dict (id=>bool)
    seen = dict(((f[functional_id_keyname], f['data_node']), False) for f in light_metadata.get_files())
    po = sdpipelineprocessing.ProcessingObject(remove, functional_id_keyname, seen)
    metadata = sdpipelineprocessing.run_pipeline(metadata, po)
    return metadata


def remove(files, functional_id_keyname, seen):
    new_files = []
    for f in files:
        uniq_id = (f[functional_id_keyname], f['data_node'])  # tuple
        if not seen[uniq_id]:
            new_files.append(f)
            seen[uniq_id] = True  # mark as seen so other duplicate will be excluded (first item in the loop win)
    return new_files
