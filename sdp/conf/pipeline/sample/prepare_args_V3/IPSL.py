#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""
Contains whole variable default pipeline definition.

"""

from sppipelineutils import get_args
from sppostprocessingutils import PostProcessingPipeline, State, Transition


def get_pipeline():
    return ppp

name = 'IPSL'
ppp = PostProcessingPipeline(name)

t1 = Transition(name='suppression_variable', destination='S0200', get_args=get_args)
t2 = Transition(name='coalesce', destination='S0300', get_args=get_args)
t3 = Transition(name='overlap', destination='S0400', get_args=get_args)
t4 = Transition(name='time_axis_normalization', destination='S0500', get_args=get_args)
t5 = Transition(name='suppression_variable', destination='S0600', get_args=get_args)
t6 = Transition(name='copy', destination='S0700', get_args=get_args)
t7 = Transition(name='cdscan', destination='S0800', get_args=get_args)
t8 = Transition(name='latest', destination='S0900', get_args=get_args)
t9 = Transition(name='mapfile', destination='S1000', get_args=get_args)
t10 = Transition(name='publication', destination='S1100', get_args=get_args)

s1 = State(name='S0100', transition=t1, initial=True)
s2 = State(name='S0200', transition=t2)
s3 = State(name='S0300', transition=t3)
s4 = State(name='S0400', transition=t4)
s5 = State(name='S0500', transition=t5)
s6 = State(name='S0600', transition=t6)
s7 = State(name='S0700', transition=t7)
s8 = State(name='S0800', transition=t8)
s9 = State(name='S0900', transition=t9)
s10 = State(name='S1000', transition=t10)
s11 = State(name='S1100', transition=None)

ppp.add(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11)
