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

import copy
import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline,State,Transition

def get_pipeline(name):
    return copy.deepcopy(pipelines[name])

# init.

pipelines={}

def f1(**generic_args):
    path=sppipelineutils.build_process_path(**generic_args)
    return {'variable_path':path}

name='CMIP5_002'
ppp=PostProcessingPipeline(name)
ppp.project='CMIP5'

t1=Transition(name='latest',destination='S1200',get_args=f1)
t2=Transition(name='latest_xml',destination='S1300',get_args=f1)
t3=Transition(name='mapfile',destination='S1400',get_args=f1)

s1=State(name='S1100',transition=t1,initial=True)
s2=State(name='S1200',transition=t2)
s3=State(name='S1300',transition=t3)
s4=State(name='S1400',transition=None)

ppp.add(s1,s2,s3,s4)

pipelines[name]=ppp
