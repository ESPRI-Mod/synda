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

import sys
import argparse
import re
import time
from fabric.api import task

sys.path.append("..")

from testlib.svtestutils import fabric_run, task_exec, Testset, title
import testlib.svtestcommon as tc

def run():
    task_exec(tc.stop) 
    task_exec(tc.disable_download) 
    task_exec(tc.do_not_print_domain_inconsistency) 
    task_exec(tc.configure) 
    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    task_exec(tc.reset) 

    task_exec(tc.retrieve_parameters)

    task_exec(normal_discovery)
    task_exec(check_normal_discovery_result)
    task_exec(incremental_discovery)
    #task_exec(check_incremental_discovery_result)
    #task_exec(check_that_incremental_discovery_fetched_only_the_delta)

    print 'Incremental discovery took %d minutes to complete'%999

@task
def normal_discovery():
    fabric_run('synda install -y --timestamp_right_boundary %s -s %s'%(first_discovery_timestamp_right_boundary,testset.selection_file,))

@task
def check_normal_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 19525')

@task
def incremental_discovery():
    fabric_run('synda install -i -y --timestamp_right_boundary %s -s %s'%(second_discovery_timestamp_right_boundary,testset.selection_file,))

@task
def check_incremental_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 2473')

@task
def check_that_incremental_discovery_fetched_only_the_delta():
    fabric_run('test ! -f grep SYDPROXY-100 /var/log/synda/sdt/discovery.log')

# init.
    
testset=Testset()
testset.selection_file='./resource/template/heavy/heavy.txt'

first_discovery_timestamp_right_boundary='2012-03-19T01:00:00Z'
second_discovery_timestamp_right_boundary='2012-03-25T01:00:00Z'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
