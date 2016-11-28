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

sys.path.append("..")

from testlib.svtestutils import fabric_run, task_exec, Testset, title
import testlib.svtestcommon as tc

def run():

    # check env.

    task_exec(tc.execute_basic_sdt_command)
    task_exec(tc.execute_basic_sdp_command)
    task_exec(tc.check_sdt_version)
    task_exec(tc.check_sdp_version)


    # download & IPSL pipeline (CMIP5)

    prepare()
    discovery('CMIP5')
    download('CMIP5')
    IPSL_postprocessing('CMIP5')


    # download & IPSL pipeline (CORDEX)

    prepare()
    discovery('CORDEX')
    download('CORDEX')
    IPSL_postprocessing('CORDEX')


    # download & IPSL pipeline & CDF pipeline (CMIP5)

    prepare()
    download('CMIP5')
    IPSL_postprocessing('CMIP5')
    CDF_postprocessing('CMIP5')


    print 'Test complete successfully !'

def prepare():
    task_exec(tc.stop_all)
    task_exec(tc.disable_eventthread)
    task_exec(tc.reset_all)

def exec_wrapper(name):
    fu=globals()[name] 
    task_exec(fu)

def discovery(project):
    exec_wrapper('install_%s'%project)
    exec_wrapper('check_install_result_%s'%project)

def download(project):
    task_exec(tc.enable_download)
    task_exec(tc.start_sdt)
    time.sleep(time_to_wait_for_download) # give some time for the file to be downloaded
    exec_wrapper('check_download_result_%s'%project)

def IPSL_postprocessing(project):
    task_exec(tc.enable_eventthread)
    transfer_events(project)
    task_exec(start_pp_pipelines)
    task_exec('check_IPSL_postprocessing_result_%s'%project)

def CDF_postprocessing(project):
    task_exec(trigger_CDF)
    transfer_events(project)
    task_exec('check_CDF_postprocessing_result_%s'%project)

def transfer_events(project):
    # transfer events from SDT to SDP
    task_exec(tc.start_sdp)
    time.sleep(time_to_wait_for_transferring_event) # give some time for pp events to be transfered from SDT to SDP
    task_exec(check_transfer_events_result)

# -- tasks -- #

@task
def install_CMIP5():
    fabric_run('sudo synda install -y -s ./resource/template/CMIP5.txt')

@task
def check_install_result_CMIP5():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 4')

@task
def check_download_result_CMIP5():

    # check that all files are done
    fabric_run('test $(synda list limit=0 -f | grep "^done" | wc -l) -eq 4')

    # check that corresponding events have been created
    fabric_run("""test $(sqlite3  /var/lib/synda/sdt/sdt.db "select * from event where status='new'" | wc -l) -eq 6""")

@task
def check_transfer_events_result():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdt/sdt.db "select * from event where status='old'" | wc -l) -eq 6""")

@task
def install_CORDEX():
    fabric_run('sudo synda install -y -s ./resource/template/CORDEX.txt')

@task
def check_install_result_CORDEX():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 4')

@task
def trigger_CDF():
    fabric_run('sudo synda pexec cdf -s ./resource/template/CMIP5.txt')

@task
def start_pp_pipelines():
    fabric_run('synda_wo -x start')
    fabric_run('test -f /tmp/foobar')

@task
def fake():
    fabric_run('test ! -f /srv/synda/sdt/data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc')

# init.

time_to_wait_for_download=50
time_to_wait_for_transferring_event=20
scripts_pp='./resource/scripts_pp'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
