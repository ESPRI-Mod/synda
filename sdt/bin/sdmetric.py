#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module displays performance and disk usage coarse-grained metrics (model, data_node, project).

Note
    For fine-grained metrics about a specific data selection (e.g. selection file), see sdstat module.

Also see
    sdstat
"""

import argparse
import sdapp
import sdfilequery
import humanize
from tabulate import tabulate

def format_size(size):
    size_mib=size/1024.0/1024.0   # go from bytes to mebibyte
    size_mib='% 4.2f'%size_mib    # set float precision
    return size_mib

def print_rate(groupby,project_,dry_run=False):

    # retrieve metrics from local database
    li=sdfilequery.get_metrics(groupby,'rate',project_,dry_run=dry_run)

    if dry_run:
        return

    # prepare
    unit='MiB/s'                               # prepare unit
    headers=[groupby.title(),'Rate (%s)'%unit] # prepare headers
    li=[(t[0],format_size(t[1])) for t in li]  # prepare body

    # print
    print tabulate(li,headers=headers,tablefmt="plain",numalign="decimal")

def print_size(groupby,project_,dry_run=False):

    # retrieve metrics from local database
    li=sdfilequery.get_metrics(groupby,'size',project_,dry_run=dry_run)

    if dry_run:
        return

    # prepare
    headers=[groupby.title(),'Size']                                      # prepare headers
    li=[(t[0],humanize.naturalsize(t[1],gnu=False)) for t in li]        # prepare body

    # print
    print tabulate(li,headers=headers,tablefmt="plain",numalign="decimal")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
