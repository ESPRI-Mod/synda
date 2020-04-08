#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains metadata common routine.

Notes
    - low memory compatible
    - sdmdcommon stands for 'SynDa MetaData COMMON'.

"""
from sdt.bin.commons.facets import sdlmattrfilter


def get_attributes(metadata, attr_name):
    li = []
    # create light metadata with one column only
    light_metadata = sdlmattrfilter.run(metadata, [attr_name])
    # load metadata in memory (dict), but as metadata only contain one attribute
    # it should not exceed the available memory.
    for f in light_metadata.get_files():
        attr_val = f[attr_name]
        li.append(attr_val)  # duplicate metadata in memory (list). Means metadata are loaded twice simultaneously.
    return li
