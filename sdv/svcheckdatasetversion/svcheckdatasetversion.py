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

import sys
import argparse
import re
import time
from fabric.api import task
from fabric.api import execute as task_exec

sys.path.append("..")

from testlib.svtestutils import fabric_run
import testlib.svtestcommon as tc

def run():

    task_exec(tc.configure_task) 
    #task_exec(restart) 

    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)
    #task_exec(check_dataset_version)
    #task_exec(check_dataset_version)

    #time.sleep(150) # give some time for the file to be downloaded (default 300)

    #task_exec(check_dataset_version)
    #task_exec(check_dataset_version)
    #task_exec(check_dataset_version)
    #task_exec(check_dataset_version)

@task
def check_dataset_version():
    fabric_run('synda check dataset_version')

@task
def check_dataset_version():
    fabric_run('sudo synda install -y cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac')

@task
def check_dataset_version():
    fabric_run('test -f /tmp/foobar')

@task
def check_dataset_version():
    fabric_run('sudo synda stat CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac | grep "Done files count: 1"')

@task
def check_dataset_version():
    fabric_run('sudo synda remove -y CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac')

@task
def check_dataset_version():
    fabric_run('test ! -f /srv/synda/sdt/data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc')

# init.

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
