#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains *remote* variable display routines."""

import os
import argparse
import sdapp
import sdvariable
from tabulate import tabulate

def print_list(datasets,limit=None):
    li=get_variable_list(datasets,limit)
    print tabulate(li,tablefmt="plain")

def print_details(d):
    TODO
    print "Dataset: %s"%d['id']
    print "Dataset total size=%i"%int(d['size'])

    """
    # Disable as it seems to be more ergonomic not to group datasets and files listing
    # (when user wants datasets listing, he ask for it, when he wants files listing he ask for it with a new request)

    print
    print "Dataset files list:"
    for f in d.files:
        print "%-15s  %s"%(f['size'],f['filename'])
    print "%i files found."%(len(d.files),)
    """

def get_variable_list(datasets,limit=None):
    li=[]

    for d in datasets:
        for v in d['variable']:
            variable_functional_id=sdvariable.build_variable_functional_id(d['dataset_functional_id'],v) # note that variable is NOT an ESGF official identifier
            li.append([variable_functional_id])

            if limit is not None:
                if len(li)>=limit:
                    return li

    return li

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
