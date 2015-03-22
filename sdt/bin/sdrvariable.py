#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdrvariable.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains *remote* variable display routines."""

import os
import argparse
import sdapp
import sdvariable
from tabulate import tabulate

def print_list(datasets):
    li=[]
    for d in datasets:
        for v in d['variable']:
            variable_functional_id=sdvariable.build_variable_functional_id(d['dataset_functional_id'],v) # note that variable is NOT an ESGF official identifier
            li.append([variable_functional_id])
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
