#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module filter attributes (lowmem compatible).

Note
    sdlmattrfilter means 'SynDa Low Mem ATTRibute FILTER'.
"""

import sdapp
import sdconst
import sdpipelineprocessing

def run(metadata,attrs_to_keep):

    assert not isinstance(metadata.store,list)

    metadata_cpy=metadata.copy() # prevent modify original data

    assert not isinstance(metadata_cpy.store,list)

    light_metadata=sdpipelineprocessing.run_pipeline(sdconst.PROCESSING_FETCH_MODE_GENERATOR,metadata_cpy,attribute_filter,attrs_to_keep)
    return light_metadata

def attribute_filter(files,keeped_attrs):
    new_files=[]
    for f in files:
        new_files.append(dict((k, f[k]) for k in keeped_attrs))
    return new_files
