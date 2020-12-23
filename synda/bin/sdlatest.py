#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains routines related to 'latest' flag.

Note
    Routines dealing with both 'status' and 'latest' flag are stored in sddatasetflag module.
"""

import sdapp
import sdlatestquery
import sddatasetflag
import sddatasetdao
import sdtools

def print_latest_datasets_full():
    print_latest_datasets(True)

def print_latest_datasets_recent():
    print_latest_datasets(False)

def print_latest_datasets(full):
    for d in sdlatestquery.get_latest_datasets(full):
        print d.get_full_local_path()

def set_latest_flag(path):
    """This method is used to manually set the 'latest' flag.

    Note
        Not used.
    """

    d=sddatasetdao.get_dataset(path=path,raise_exception_if_not_found=False) # retrieve dataset from database
    if d is not None:
        if d.latest==True:
            print "'latest' flag is already set for this dataset"
        else:
            sddatasetflag.update_latest_flag(d,force_latest=True) # warning: this method modifies the dataset in memory (and in database too)
    else:
        sdtools.print_stderr('Dataset not found')
