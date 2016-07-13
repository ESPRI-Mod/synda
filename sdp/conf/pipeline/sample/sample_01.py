#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains sample_01 pipeline definition."""

import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline,State,Transition

def get_pipeline():
    return ppp

def set_variable_path_type(kw):
    assert kw.variable!='' # additional check just in case
    kw.path_type='variable'

# init.

def f1(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_process_path(kw)
    return {'project':kw.project,'variable_path':path}
def f2(kw):
    set_variable_path_type(kw)
    src_path=sppipelineutils.build_mirror_path(kw)
    dest_path=sppipelineutils.build_process_path(kw)
    return {'project':kw.project,'src_variable_path':src_path,'dest_variable_path':dest_path}
def f3(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_user_path('main',kw)
    return {'project':kw.project,'variable_path':path}
def f4(kw):
    set_variable_path_type(kw)
    src_path=sppipelineutils.build_process_path(kw)
    dest_path=sppipelineutils.build_user_path('main',kw)
    return {'project':kw.project,'src_variable_path':src_path,'dest_variable_path':dest_path}
def f5(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_user_path('main',kw)
    return {'project':kw.project,'dataset_path':path}

name='sample_01'
ppp=PostProcessingPipeline(name)

t0=Transition(name='is_duplicate',destination={0:'S0300',1:'S0100'})
t1=Transition(name='time_axis_normalization',destination='S0200',get_args=f1)
t2=Transition(name='latest',destination='S0300',get_args=f5)

s0=State(name='S0090',transition=t0,initial=True)
s1=State(name='S0100',transition=t1)
s2=State(name='S0200',transition=t2)
s3=State(name='S0300',transition=None)

ppp.add(s0,s1,s2,s3)
