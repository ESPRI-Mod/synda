#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains stat generic routines."""

import sys
import argparse
import json
import humanize
import sdapp
import sdconst

def get_total(statuses):
    total={}
    total['pending']={}
    total['all']={}

    total['pending']['count']=sum(statuses[s]['count'] for s in sdconst.TRANSFER_STATUSES_PENDING)
    total['pending']['size']=sum(statuses[s]['size'] for s in sdconst.TRANSFER_STATUSES_PENDING)
    total['all']['count']=sum(statuses[s]['count'] for s in sdconst.TRANSFER_STATUSES_ALL)
    total['all']['size']=sum(statuses[s]['size'] for s in sdconst.TRANSFER_STATUSES_ALL)

    return total

def init_table():
    statuses={}

    for status in sdconst.TRANSFER_STATUSES_ALL:
        statuses[status]={}

    for status in sdconst.TRANSFER_STATUSES_ALL:
        statuses[status]['count']=0
        statuses[status]['size']=0

    return statuses

def get_statuses(files,statuses):
    """Returns size & count for each status."""

    for f in files:
        statuses[f['status']]['count']+=1
        statuses[f['status']]['size']+=int(f['size'])

    return []
