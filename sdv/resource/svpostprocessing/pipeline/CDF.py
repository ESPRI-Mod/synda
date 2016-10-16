#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains 'dataset latest' pipeline definition."""

import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline, State, Transition


def get_pipeline():
    return ppp


def set_variable_path_type(kw):
    assert kw.variable != ''
    kw.path_type = 'variable'


def f1(kw):
    set_variable_path_type(kw)
    src_path = sppipelineutils.build_process_path(kw)
    dest_path = sppipelineutils.build_user_path('interpolated', kw)
    return {'project': kw.project, 'src_variable_path': src_path, 'dest_variable_path': dest_path}


def f2(kw):
    set_variable_path_type(kw)
    path = sppipelineutils.build_user_path('interpolated', kw)
    return {'project': kw.project, 'dataset_path': path}


def f3(kw):
    set_variable_path_type(kw)
    src_path = sppipelineutils.build_user_path('interpolated', kw)
    dest_path = sppipelineutils.build_user_path('bias-adjusted', kw)
    return {'project':  kw.project, 'src_variable_path': src_path, 'dest_variable_path': dest_path,
            'variable': kw.variable}


def f4(kw):
    set_variable_path_type(kw)
    path = sppipelineutils.build_user_path('bias-adjusted', kw)
    return {'project': kw.project, 'variable_path': path, 'variable': kw.variable}


def f5(kw):
    set_variable_path_type(kw)
    path = sppipelineutils.build_user_path('bias-adjusted', kw)
    return {'project': kw.project, 'dataset_path': path}

name = 'CDF'
ppp = PostProcessingPipeline(name)

t1 = Transition(name='spatial_interpolation', destination='S2200', get_args=f1)
t2 = Transition(name='latest', destination='S2300', get_args=f2)
t3 = Transition(name='correction_cdft', destination='S2400', get_args=f3)
t4 = Transition(name='standardization', destination='S2500', get_args=f4)
t5 = Transition(name='latest', destination='S2600', get_args=f5)

s1 = State(name='S2100', transition=t1, initial=True)
s2 = State(name='S2200', transition=t2)
s3 = State(name='S2300', transition=t3)
s4 = State(name='S2400', transition=t4)
s5 = State(name='S2500', transition=t5)
s6 = State(name='S2600', transition=None)

ppp.add(s1, s2, s3, s4, s5)
