#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing pipeline.

Note
    - 'spppp' means 'Synda Post-Processing Pipeline' # TODO: rename spppp.py to sppp.py
"""

import copy
import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline,State,Transition

def get_pipeline(name):
    return copy.deepcopy(pipelines[name])

# init.

pipelines={}


# 'variable complete' pipeline definition

name='CMIP5_001'
ppp=PostProcessingPipeline(name)
ppp.project='CMIP5'

def f1(**generic_args):
    dataset_pattern=sppparg.replace_product_facet(dataset_pattern) if project=='CMIP5' else dataset_pattern # product coalesce hack
    dataset_pattern=replace_product_facet(dataset_pattern,project)
    path=sppparg.get_full_path_variable(dataset_pattern,project,variable,'esgf/process')
    return {'full_path_variable':path}
def f2(**generic_args):
    input_path=sppparg.get_full_path_variable(dataset_pattern,project,variable,'esgf/mirror')
    dataset_pattern=sppparg.replace_product(dataset_pattern) if project=='CMIP5' else dataset_pattern # product coalesce hack
    output_path=sppparg.get_full_path_variable(dataset_pattern,project,variable,'esgf/process')
    return {'input_variable_path':input_path,'output_variable_path':output_path}
def f3(**generic_args):
    dataset_pattern=sppparg.remove_first_facet(dataset_pattern) # Remove project facet. WARNING: we assume all datasets start with 'project' facet (but this is not the case for some projects, e.g. obs4MIPs / RMBE.ARMBE_Wind_Direction)
    dataset_pattern=sppparg.remove_first_facet(dataset_pattern) if project in ['CMIP5','CORDEX'] else dataset_pattern # Remove product facet
    prefix='%s/%s/%s/%s'%(spconfig.data_folder,'project',project,'main')
    path=sppparg.get_full_path_variable(dataset_pattern,project,variable,prefix)
    return {'full_path_variable':path}
def f4(**generic_args):
    TODO

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

pipelines[name]=ppp


# 'dataset latest' pipeline definition

name='CMIP5_002'
ppp=PostProcessingPipeline(name)
ppp.project='CMIP5'

t1=Transition(name='latest',destination='S1200',workdir='merge')
t2=Transition(name='latest_xml',destination='S1300',workdir='merge')
t3=Transition(name='mapfile',destination='S1400',workdir='merge')

s1=State(name='S1100',transition=t1,initial=True)
s2=State(name='S1200',transition=t2)
s3=State(name='S1300',transition=t3)
s4=State(name='S1400',transition=None)

ppp.add(s1,s2,s3,s4)

pipelines[name]=ppp
