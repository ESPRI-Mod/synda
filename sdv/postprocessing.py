#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains user acceptance testing (UAT) routines."""

import argparse
import re
import time
import fabric.api
from testcommon import fabric_run

def run():

    fabric.api.execute(configure_task) 
    #fabric.api.execute(restart) 

    fabric.api.execute(execute_basic_command)
    fabric.api.execute(check_version)
    #fabric.api.execute(check_dataset_version)
    #fabric.api.execute(check_dataset_version)

    #time.sleep(150) # give some time for the file to be downloaded (default 300)

    #fabric.api.execute(check_dataset_version)
    #fabric.api.execute(check_dataset_version)
    #fabric.api.execute(check_dataset_version)
    #fabric.api.execute(check_dataset_version)

@fabric.api.task
def check_dataset_version():
    fabric_run('synda check dataset_version')

@fabric.api.task
def check_dataset_version():
    fabric_run('sudo synda install -y cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac')

@fabric.api.task
def check_dataset_version():
    fabric_run('test -f /tmp/foobar')

@fabric.api.task
def check_dataset_version():
    fabric_run('sudo synda stat CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac | grep "Done files count: 1"')

@fabric.api.task
def check_dataset_version():
    fabric_run('sudo synda remove -y CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac')

@fabric.api.task
def check_dataset_version():
    fabric_run('test ! -f /srv/synda/sdt/data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc')

# init.
sdt_version='3.6'
pp_password='bar'
esgf_password='foo'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
