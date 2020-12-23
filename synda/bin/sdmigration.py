#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains upgrade procedures."""

import os
import re
import sys
import sdapp

def MIGR0001():
    """
    description:
        - populate dataset table
        - populate dataset_id column of transfer table
    """
    CDatabaseMigration.populateDataset()

def execProc(proc_name):

    sdlog.info("SYNDMIGR-231","routine '%s' starts"%proc_name)

    try:
        getattr(proc_name.upper())()
    except Exception,e:
        raise

    sdlog.info("SYNDMIGR-232","routine '%s' completes successfully"%proc_name)

# module init

if not tableAlreadyPopulated(tablename="version"):
    insertVersion()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--procedure',required=True,default=None)
    args = parser.parse_args()
