#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains stream related routines."""

import sdbuffer
import sdparse
import sdexception

def get_stream(parameter=None,selection_file=None,no_default=True,raise_exception_if_empty=False):
    """
    TODO: merge me with syndautils.get_stream
    """

    if parameter is None:
        parameter=[]

    buffer=sdbuffer.get_selection_file_buffer(parameter=parameter,path=selection_file)


    if len(buffer.lines)==0:
        # we come here when user selected nothing (neither from stdin neither from selection file neither from arg)

        if raise_exception_if_empty:
            raise sdexception.EmptySelectionException()


    selection=sdparse.build(buffer,load_default=(not no_default))
    stream=selection.to_stream()

    return stream # aka facets_groups
