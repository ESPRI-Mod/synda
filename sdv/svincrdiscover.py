#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains UAT test for incremental discovery."""

import argparse
import re
import time
import fabric.api
from testcommon import fabric_run

def run():

    fabric.api.execute(stop) 
    fabric.api.execute(configure_task) 
    fabric.api.execute(execute_basic_command)
    fabric.api.execute(check_version)

    fabric.api.execute(normal_discovery)
    fabric.api.execute(check_normal_discovery_result)
    #time.sleep(150) # give some time for the file to be downloaded (default 300)

@fabric.api.task
def normal_discovery():
    master_id='cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1'
    date_t1='2015-11-01T01:00:00Z'

    fabric_run('synda install -y master_id=%s replica=false to=%s'%(master_id,date_t1))

@fabric.api.task
def check_normal_discovery_result():
    fabric_run('synda install -y cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac')

@fabric.api.task
def check_dataset_version():
    fabric_run('test -f /tmp/foobar')

@fabric.api.task
def check_dataset_version():
    fabric_run('synda stat CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac | grep "Done files count: 1"')

@fabric.api.task
def check_dataset_version():
    fabric_run('synda remove -y CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac')

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
