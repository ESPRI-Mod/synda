#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains 'variable complete' pipeline definition."""

import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline,State,Transition

def get_pipeline():
    return ppp

def set_variable_path_type(kw):
    assert kw['variable']!='' # additional check just in case
    kw['path_type']='variable'

# init.

name='CMIP5_001'
ppp=PostProcessingPipeline(name)
ppp.project='CMIP5'

TODO_CHECK => see if is ok not to send generic args project, variable and dataset_pattern as before

TODO_CHECK
def f1(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_process_path(kw)
    return {'variable_path':path}
def f2(kw):
    set_variable_path_type(kw)
    src_path=sppipelineutils.build_mirror_path(kw)
    dest_path=sppipelineutils.build_process_path(kw)
    return {'src_variable_path':src_path,'dest_variable_path':dest_path}
def f3(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_user_path(kw)
    return {'variable_path':path}
def f4(kw):
    set_variable_path_type(kw)
    src_path=sppipelineutils.build_process_path(kw)
    dest_path=sppipelineutils.build_user_path(kw)
    return {'src_variable_path':src_path,'dest_variable_path':dest_path}

t1=Transition(name='suppression_variable',destination='S0200',get_args=f1)
t2=Transition(name='coalesce',destination='S0300',get_args=f2)
t3=Transition(name='overlap',destination='S0400',get_args=f1)
t4=Transition(name='time_axis_normalization',destination='S0500',get_args=f1)
t5=Transition(name='cdscan',destination='S0600',get_args=f1)
t6=Transition(name='suppression_variable',destination='S0700',get_args=f3)
t7=Transition(name='copy',destination='S0800',get_args=f4)

s1=State(name='S0100',transition=t1,initial=True)
s2=State(name='S0200',transition=t2)
s3=State(name='S0300',transition=t3)
s4=State(name='S0400',transition=t4)
s5=State(name='S0500',transition=t5)
s6=State(name='S0600',transition=t6)
s7=State(name='S0700',transition=t7)
s8=State(name='S0800',transition=None)

ppp.add(s1,s2,s3,s4,s5,s6,s7,s8)
