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
import fabric.api
from fabric.api import task
from fabric.api import execute as task_exec

sys.path.append("..")

from testlib.svtestutils import fabric_run
import testlib.svtestcommon as tc

def run():
    task_exec(confirm_test_platform_is_ready)

    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    task_exec(reset_test_platform)

    task_exec(tc.stop_sdt)
    task_exec(tc.stop_sdp)

    # discovery
    task_exec(install_CMIP5)
    task_exec(check_CMIP5_installation_result)
    task_exec(install_CORDEX)
    task_exec(check_CORDEX_installation_result)

    # download
    task_exec(tc.start_sdt)
    time.sleep(300) # give some time for the file to be downloaded
    task_exec(check_download_result)

    # pexec
    task_exec(trigger_CDF)
    task_exec(check_CDF_trigger_result)

    # pp events transfer
    task_exec(tc.start_sdp)
    time.sleep(50) # give some time for pp events to be transfered from SDT to SDP
    task_exec(check_pp_events_transfer_result)

    # start pp pipelines
    task_exec(start_pp_pipelines)
    task_exec(check_pp_pipelines_result)

    print 'Test complete successfully !'

@task
def confirm_test_platform_is_ready():
    fabric_run('sudo synda install -y cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac')

@task
def reset_test_platform():
    fabric_run('%s'%reset_script)

@task
def install_CMIP5():
    fabric_run('test -f /tmp/foobar')

@task
def install_CORDEX():
    fabric_run('sudo synda stat CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac | grep "Done files count: 1"')

@task
def trigger_CDF():
    fabric_run('sudo synda remove -y CMIP5 MPI-M MPI-ESM-LR decadal1995 mon baresoilFrac')

@task
def start_pp_pipelines():
    fabric_run('synda_wo -x start')

@task
def fake():
    fabric_run('test ! -f /srv/synda/sdt/data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc')

# init.

reset_script='./resource/reset.sh'
scripts_pp='./resource/scripts_pp'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
