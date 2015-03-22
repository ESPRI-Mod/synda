#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdmigration.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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

    sdlog.log("SDMIGR-INF231","routine '%s' starts"%proc_name)

    try:
        getattr(proc_name.upper())()
    except Exception,e:
        raise

    sdlog.log("SDMIGR-INF232","routine '%s' completes successfully"%proc_name)

# module init

if not tableAlreadyPopulated(tablename="version"):
    insertVersion()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--procedure',required=True,default=None)
    args = parser.parse_args()
