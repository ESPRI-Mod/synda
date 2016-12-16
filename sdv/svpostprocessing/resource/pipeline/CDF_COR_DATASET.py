#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""
Contains whole variable pipeline definition for tCDF.

"""

from sppipelineutils import get_args
from sppostprocessingutils import PostProcessingPipeline, State, Transition


def get_pipeline():
    return ppp

name = 'CDF_COR_DATASET'
ppp = PostProcessingPipeline(name)

t1 = Transition(name='latest', destination='S3600', get_args=get_args)

s1 = State(name='S3500', transition=t1, initial=True)
s2 = State(name='S3600', transition=None)

ppp.add(s1, s2)
