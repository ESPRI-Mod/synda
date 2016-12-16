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

name = 'CDF_COR'
ppp = PostProcessingPipeline(name)

t1 = Transition(name='correction_cdft', destination='S3200', get_args=get_args)
t2 = Transition(name='standardization', destination='S3300', get_args=get_args)
t3 = Transition(name='time_axis_normalization', destination='S3400', get_args=get_args)
#t4 = Transition(name='qc_qa', destination='S3500', get_args=get_args)
t4 = Transition(name='copy', destination='S3500', get_args=get_args)
t5 = Transition(name='latest', destination='S3600', get_args=get_args)

s1 = State(name='S3100', transition=t1, initial=True)
s2 = State(name='S3200', transition=t2)
s3 = State(name='S3300', transition=t3)
s4 = State(name='S3400', transition=t4)
s5 = State(name='S3500', transition=t5)
s6 = State(name='S3600', transition=None)

ppp.add(s1, s2, s3, s4, s5, s6)
