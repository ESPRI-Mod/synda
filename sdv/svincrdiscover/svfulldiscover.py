#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains UAT test for full discovery."""

import sys
import argparse
import re
import time
from fabric.api import task

sys.path.append("..")

from testlib.svtestutils import fabric_run, task_exec, Testset, title, SDTimer
import testlib.svtestcommon as tc

def run():
    task_exec(tc.stop) 
    task_exec(tc.disable_download) 
    task_exec(tc.do_not_print_domain_inconsistency) 
    task_exec(tc.configure) 
    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    task_exec(tc.reset_sdt) 

    task_exec(tc.retrieve_parameters)

    task_exec(full_discovery_step_1)
    task_exec(check_fds1_result)
    start_time=SDTimer.get_time()
    task_exec(full_discovery_step_2)
    elapsed_time=SDTimer.get_elapsed_time(start_time)
    task_exec(check_fds2_result)
    task_exec(check_that_full_discovery_fetched_all_metadata)

    print 'Full discovery took %d seconds to complete'%elapsed_time

    print 'Test complete successfully !'

@task
def full_discovery_step_1():
    fabric_run('synda install -y --timestamp_right_boundary %s -s %s'%(first_discovery_timestamp_right_boundary,testset.selection_file,))

@task
def check_fds1_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 19525')

@task
def full_discovery_step_2():
    fabric_run('synda install -y --timestamp_right_boundary %s -s %s'%(second_discovery_timestamp_right_boundary,testset.selection_file,))

@task
def check_fds2_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 19566')

@task
def check_that_full_discovery_fetched_all_metadata():

    # check number of file retrieved from ESGF index during first discovery
    fabric_run("test $(grep SDSEARCH-584 /var/log/synda/sdt/discovery.log | head -1 | sed 's/^.*(\(.*\) files)/\\1/') -eq 19525")

    # check number of file retrieved from ESGF index during second discovery
    fabric_run("test $(grep SDSEARCH-584 /var/log/synda/sdt/discovery.log | tail -1 | sed 's/^.*(\(.*\) files)/\\1/') -eq 19566")

# init.
    
testset=Testset()
testset.selection_file='./resource/template/JT_T1_CMIP5.txt'

first_discovery_timestamp_right_boundary='2012-03-19T01:00:00Z'
second_discovery_timestamp_right_boundary='2012-03-25T01:00:00Z'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',nargs='?')
    args = parser.parse_args()

    if args.action is None:
        run()
    elif args.action=='reset':

        task_exec(tc.stop) 
        task_exec(tc.reset_sdt) 
        task_exec(tc.disable_download) 
        task_exec(tc.do_not_print_domain_inconsistency) 
        task_exec(tc.set_dkrz_indexes) 

        sys.stderr.write('Ok\n')
