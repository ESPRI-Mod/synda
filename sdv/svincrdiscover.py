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
from fabric.api import task
from svtestutils import fabric_run, task_exec, TestSet
import svtestcommon as tc

def run():
    task_exec(tc.stop) 
    task_exec(tc.disable_download) 
    task_exec(tc.configure_task) 
    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    task_exec(tc.reset) 
    light_test()

    task_exec(tc.reset) 
    heavy_test()

def light_test():

    print 'At T1 (some months ago), a normal (full) discovery is performed'
    task_exec(normal_discovery)
    task_exec(check_normal_discovery_result)

    print 'A few weeks pass, without any discovery being run..'
    time.sleep(5)

    print 'At T2 (current time), a incremental discovery is performed'
    task_exec(incremental_discovery)
    task_exec(check_incremental_discovery_result)

def heavy_test():
    task_exec(install_large_template)
    task_exec(install_large_template_full_discovery_db_backup)
    task_exec(incremental_discovery)
    task_exec(check_incremental_discovery_result)
    task_exec(check_that_incremental_discovery_fetched_only_the_delta)
    print 'Incremental discovery took %d minutes to complete'%999

@task
def normal_discovery():
    date_t1='2015-11-01T01:00:00Z'
    fabric_run('synda install -y %s to=%s'%(light_testset.parameter,date_t1))

@task
def check_normal_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 2473')

@task
def incremental_discovery():
    fabric_run('synda install -i -y %s'%(light_testset.parameter,))

@task
def check_incremental_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq TODO')

@task
def install_large_template():
    fabric_run('TODO')

@task
def install_large_template_full_discovery_db_backup():
    fabric_run('TODO')

@task
def check_that_incremental_discovery_fetched_only_the_delta():
    fabric_run('test ! -f grep SYDPROXY-100 /var/log/synda/sdt/discovery.log')

# init.
    
light_testset=Testset()
light_testset.parameter='CMIP5 output1 MOHC HadGEM2-ES rcp85 mon atmos Amon r1i1p1'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
