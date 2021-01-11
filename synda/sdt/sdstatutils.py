#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains stat generic routines."""
from synda.source.config.process.download.constants import TRANSFER


def get_total(statuses):

    total = {'pending': {}, 'all': {}}

    total['pending']['count'] = sum(statuses[s]['count'] for s in TRANSFER["statuses"]['pending'])
    total['pending']['size'] = sum(statuses[s]['size'] for s in TRANSFER["statuses"]['pending'])
    total['all']['count'] = sum(statuses[s]['count'] for s in TRANSFER["statuses"]["all"])
    total['all']['size'] = sum(statuses[s]['size'] for s in TRANSFER["statuses"]['all'])

    return total


def init_table():

    statuses = {}

    for status in TRANSFER["statuses"]['all']:
        statuses[status] = {}

    for status in TRANSFER["statuses"]['all']:
        statuses[status]['count'] = 0
        statuses[status]['size'] = 0

    return statuses


def get_statuses(files, statuses):
    """Returns size & count for each status."""

    for f in files:
        statuses[f['status']]['count'] += 1
        statuses[f['status']]['size'] += int(f['size'])

    return []
