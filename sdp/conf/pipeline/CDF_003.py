#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains 'dataset latest' pipeline definition."""

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
    src_path=sppipelineutils.build_process_path(kw)
    dest_path=sppipelineutils.build_user_path('interpolated',kw)
    return {'project':kw.project,'src_variable_path':src_path,'dest_variable_path':dest_path}
def f2(kw):
    set_variable_path_type(kw)
    path=sppipelineutils.build_user_path('interpolated',kw)
    return {'project':kw.project,'dataset_path':path}

name='CDF_003'
ppp=PostProcessingPipeline(name)

t1=Transition(name='spatial_interpolation',destination='S2200',get_args=f1)
t1=Transition(name='latest',destination='S2300',get_args=f2)

s1=State(name='S2100',transition=t1,initial=True)
s2=State(name='S2200',transition=t1,initial=True)
s3=State(name='S2300',transition=None)

ppp.add(s1,s2,s3)

