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

from testlib.svtestutils import fabric_run, task_exec, title
import testlib.svtestcommon as tc

def run():
    title('Performing light test')

    task_exec(tc.stop) 
    task_exec(tc.disable_download) 
    task_exec(tc.configure) 
    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    task_exec(tc.reset) 

    print 'At T1 (some months ago), a normal (full) discovery is performed'
    task_exec(normal_discovery)
    task_exec(check_normal_discovery_result)

    print 'A few weeks pass, without any discovery being run..'

    time.sleep(5)

    print

    print 'At T2 (current time), an incremental discovery is performed'
    task_exec(incremental_discovery)
    task_exec(check_incremental_discovery_result)

    print 'Test complete successfully'

@task
def normal_discovery():
    fabric_run('synda install -y -s %s'%(testset_with_right_boundary,))

@task
def check_normal_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 2473')

@task
def incremental_discovery():
    fabric_run('synda install -i -y -s %s'%(full_testset,))

@task
def check_incremental_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 2474')

# init.

testset_with_right_boundary='./resource/template/light/light_with_right_boundary.txt'
full_testset='./resource/template/light/light_full.txt'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
