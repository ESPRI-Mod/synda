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
import sdproduct
from sdtools import print_stderr
from sdtypes import Event

def submit(order_name,project,model,dataset,variable='',filename='',commit=True): # TODO: replace single quote with None and move 'None2SingleQuote' processing inside Event object (and add comment about why we use single quote instead of None in event table !!!)

    event_name=order_name

    dataset_pattern=sdproduct.replace_output12_product_with_wildcard(dataset)
    filename_pattern=filename

    sdlog.info("SDPPORDE-001","'%s' triggered (%s,%s)"%(event_name,dataset_pattern,variable))

    event=Event(name=event_name)

    event.project=project
    event.model=model
    event.dataset_pattern=dataset_pattern
    event.variable=variable
    event.filename_pattern=filename_pattern
    event.crea_date=sdtime.now()
    event.priority=sdconst.DEFAULT_PRIORITY

    sdeventdao.add_event(event,commit=commit)
