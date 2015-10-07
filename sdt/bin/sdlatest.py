#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains routines related to 'latest' flag."""

import sdapp
import sdlatestquery

def print_latest_datasets_full():
    print_latest_datasets(True)

def print_latest_datasets_recent():
    print_latest_datasets(False)

def print_latest_datasets(full):
    for d in sdlatestquery.get_latest_datasets(full):
        print d.get_full_local_path()
