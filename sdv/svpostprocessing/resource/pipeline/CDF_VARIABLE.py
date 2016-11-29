#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""
Contains variable only pipeline definition for tCDF.

"""

from sppipelineutils import get_args
from sppostprocessingutils import PostProcessingPipeline, State, Transition


def get_pipeline():
    return ppp

name = 'CDF_VARIABLE'
ppp = PostProcessingPipeline(name)

t1 = Transition(name='spatial_interpolation', destination='S2200', get_args=get_args)
t2 = Transition(name='correction_cdft', destination='S2300', get_args=get_args)
t3 = Transition(name='standardization', destination='S2400', get_args=get_args)

s1 = State(name='S2100', transition=t1, initial=True)
s2 = State(name='S2200', transition=t2)
s3 = State(name='S2300', transition=t3)
s4 = State(name='S2400', transition=None)

ppp.add(s1, s2, s3, s4)
