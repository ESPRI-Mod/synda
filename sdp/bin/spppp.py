#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: spppp.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing pipeline.

Notes
    - 'spppp' means 'Synchro-Data Post-Processing Pipeline'
"""

import copy
from sppostprocessingutils import PostProcessingPipeline,State,Transition

def get_pipeline(name):
    return copy.deepcopy(pipelines[name])

# init.

pipelines={}


# 'variable complete' pipeline definition

name='CMIP5_001'
ppp=PostProcessingPipeline(name)
ppp.project='CMIP5'

t1=Transition(name='suppression_variable',destination='S0200',workdir='process')
t2=Transition(name='coalesce',destination='S0300')
t3=Transition(name='overlap',destination='S0400',workdir='process')
t4=Transition(name='time_axis_normalization',destination='S0500',workdir='process')
t5=Transition(name='cdscan',destination='S0600',workdir='process')
t6=Transition(name='suppression_variable',destination='S0700',workdir='merge')
t7=Transition(name='copy',destination='S0800',workdir='process')

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
