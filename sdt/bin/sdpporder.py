#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains post-processing order related routines.

Note
    'sdpporder' means 'SynDa Post-Processing order'
"""

import argparse
import sdeventdao
import sdconst
import sdtime
import sdlog
from sdtools import print_stderr
from sdtypes import Event

def submit_many(type_,dataset):
    for d in datasets:
        for v in d['variable']:

def submit(order_name,type_,project,model,dataset_pattern,variable='',commit=True):
    event_name="%s_"%(type_,task_name) # sample => cdf_dataset

    sdlog.info("SDUDEVEN-001","'%s' triggered (%s,%s)"%(dataset_pattern,variable))

    event=Event(name=event_name)
    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=variable
    event.filename_pattern=''
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY
    sdeventdao.add_event(event,commit=commit)
