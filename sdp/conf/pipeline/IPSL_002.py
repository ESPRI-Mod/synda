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

def set_dataset_path_type(kw):
    assert kw.variable=='' # additional check just in case
    kw.path_type='dataset'

# init.

def f1(kw):
    set_dataset_path_type(kw)
    path=sppipelineutils.build_user_path('main',kw)
    return {'project':kw.project,'model':kw.model,'dataset_path':path}
def f3(kw):
    set_dataset_path_type(kw)
    path=sppipelineutils.build_user_path('merge',kw)
    return {'project':kw.project,'dataset_path':path}
def f4(kw):
    set_dataset_path_type(kw)
    path=sppipelineutils.build_user_path('interpolated',kw)
    return {'project':kw.project,'dataset_path':path}

name='IPSL_002'
ppp=PostProcessingPipeline(name)

t1=Transition(name='latest',destination='S1300',get_args=f1)
t2=Transition(name='mapfile',destination='S1400',get_args=f1)

s1=State(name='S1100',transition=t1,initial=True)
s2=State(name='S1300',transition=t2)
s3=State(name='S1400',transition=None)

ppp.add(s1,s2,s3)
