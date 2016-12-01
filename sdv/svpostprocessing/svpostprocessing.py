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
    discovery('CMIP5')
    download('CMIP5')
    IPSL_postprocessing('CMIP5')
    stop_worker()
    CDF_postprocessing('CMIP5')


    print 'Test complete successfully !'

def prepare():

    # stop all daemons
    task_exec(tc.stop_all)
    time.sleep(time_to_wait_for_daemon_to_stop) # give some time for daemons stop to be effective
    task_exec(check_sa_result)

    # configure
    task_exec(tc.disable_eventthread)
    task_exec(tc.set_pipeline_folder_path)
    #task_exec(tc.set_ipsl_indexes)

    # reset
    task_exec(tc.reset_all)

    # start sdp daemon
    task_exec(tc.start_sdp)
    time.sleep(10) # give some time for daemon start to be effective

    # test sdt / sdp communication
    task_exec(tc.test_sdt_sdp_communication)

    # test sdw / sdp communication
    task_exec(tc.test_sdw_sdp_communication)

    # stop all daemons
    task_exec(tc.stop_all)
    time.sleep(time_to_wait_for_daemon_to_stop) # give some time for daemons stop to be effective
    task_exec(check_sa_result)

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
    transfer_events(project,'IPSL')
    create_pp_pipelines(project,'IPSL')
    start_worker()
    time.sleep(time_to_wait_to_complete_postprocessing_jobs)
    exec_wrapper('check_IPSL_postprocessing_result_%s'%project)

def transfer_events(project,pipeline):
    """Transfer events from SDT to SDP."""
    task_exec(tc.start_sdp)
    task_exec(tc.enable_postprocessing)
    task_exec(tc.restart_sdt)
    time.sleep(time_to_wait_for_transferring_event) # give some time for pp events to be transfered from SDT to SDP
    exec_wrapper("check_transfer_events_result_%s_%s"%(project,pipeline))

def CDF_postprocessing(project):
    task_exec(trigger_CDF)
    transfer_events(project,'CDF')
    create_pp_pipelines(project,'CDF')
    start_worker()
    time.sleep(time_to_wait_to_complete_postprocessing_jobs)
    exec_wrapper('check_CDF_postprocessing_result_%s'%project)

def create_pp_pipelines(project,pipeline):
    task_exec(tc.enable_eventthread)
    task_exec(tc.restart_sdp)
    time.sleep(time_to_wait_for_ppprun_creation) # give some time for ppprun to be created
    exec_wrapper("check_ppprun_creation_result_%s_%s"%(project,pipeline))

def start_worker():
    task_exec(tc.start_sdw)

def stop_worker():
    task_exec(tc.stop_sdw)

# -------------------------- tasks -------------------------- #

@task
def check_sa_result(): # sa stands for "Stop All"
    fabric_run('! pgrep spdaemon')
    fabric_run('! pgrep synda')

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
def check_transfer_events_result_CMIP5_IPSL():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdt/sdt.db "select * from event where status='old'" | wc -l) -eq 6""")

@task
def check_ppprun_creation_result_CMIP5_IPSL():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdp/sdp.db "select * from ppprun where status in ('waiting','pause')" | wc -l) -eq 6""")

@task
def check_IPSL_postprocessing_result_CMIP5():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdp/sdp.db "select * from ppprun where status='done'" | wc -l) -eq 6""")

@task
def install_CORDEX():
    fabric_run('sudo synda install -y -s ./resource/template/CORDEX.txt')

@task
def check_install_result_CORDEX():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 10')

@task
def check_download_result_CORDEX():

    # check that all files are done
    fabric_run('test $(synda list limit=0 -f | grep "^done" | wc -l) -eq 10')

    # check that corresponding events have been created
    fabric_run("""test $(sqlite3  /var/lib/synda/sdt/sdt.db "select * from event where status='new'" | wc -l) -eq 1""")

@task
def check_transfer_events_result_CORDEX_IPSL():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdt/sdt.db "select * from event where status='old'" | wc -l) -eq 1""")

@task
def check_ppprun_creation_result_CORDEX_IPSL():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdp/sdp.db "select * from ppprun where status in ('waiting','pause')" | wc -l) -eq 1""")

@task
def check_IPSL_postprocessing_result_CORDEX():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdp/sdp.db "select * from ppprun where status='done'" | wc -l) -eq 1""")

@task
def trigger_CDF():
    fabric_run('sudo synda pexec cdf -s ./resource/template/CMIP5.txt')

@task
def check_transfer_events_result_CMIP5_CDF():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdt/sdt.db "select * from event where status='old'" | wc -l) -eq 12""")

@task
def check_ppprun_creation_result_CMIP5_CDF():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdp/sdp.db "select * from ppprun where status in ('waiting')" | wc -l) -eq 3""")

@task
def check_CDF_postprocessing_result_CMIP5():
    fabric_run("""test $(sqlite3  /var/lib/synda/sdp/sdp.db "select * from ppprun where status='done'" | wc -l) -eq 12""")

@task
def fake():
    fabric_run('test ! -f /srv/synda/sdt/data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc')

# init.

time_to_wait_for_download=300
#time_to_wait_for_download=35 # fake download mode

time_to_wait_for_transferring_event=20
time_to_wait_for_ppprun_creation=10
time_to_wait_to_complete_postprocessing_jobs=20
time_to_wait_for_daemon_to_stop=20

scripts_pp='./resource/scripts_pp'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',nargs='?')
    args = parser.parse_args()

    if args.action is None:
        run()
    elif args.action=='reset':

        prepare()

        sys.stderr.write('Ok\n')
