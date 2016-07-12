#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains CDF 'variable' pipeline definition."""

import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline,State,Transition

def get_pipeline():
    return ppp

def set_variable_path_type(kw): # FIXME: naming not clear
    assert kw.variable!='' # additional check just in case
    kw.path_type='variable'

# init.

name='CDF_001'
ppp=PostProcessingPipeline(name)

def f1(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_process_path(kw)
    return {'project':kw.project,'model':kw.model,'variable_path':path}

def f2(kw):
    set_variable_path_type(kw)
    src_path=sppipelineutils.build_process_path(kw)
    dest_path=sppipelineutils.build_user_path('interpolated',kw)
    return {'project':kw.project,'src_variable_path':src_path,'dest_variable_path':dest_path}

t1=Transition(name='spatial_interpolation',destination='S2200',get_args=f2)

s1=State(name='S2100',transition=t1,initial=True)
s2=State(name='S2200',transition=None)

ppp.add(s1,s2)
