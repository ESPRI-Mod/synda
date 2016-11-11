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
from testlib.svtestutils import fabric_run, task_exec, Testset, title
import testlib.svtestcommon as tc

def run():
    task_exec(tc.stop) 
    task_exec(tc.disable_download) 
    task_exec(tc.configure_task) 
    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    task_exec(tc.reset) 

    task_exec(install_large_template)
    task_exec(install_large_template_full_discovery_db_backup)
    task_exec(incremental_discovery)
    task_exec(check_incremental_discovery_result)
    task_exec(check_that_incremental_discovery_fetched_only_the_delta)

    print 'Incremental discovery took %d minutes to complete'%999

@task
def incremental_discovery():
    fabric_run('synda install -i -y -s %s'%(testset.selection_file,))

@task
def check_incremental_discovery_result():
    fabric_run('test $(synda list limit=0 -f | wc -l) -eq 2473')

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
    
testset=Testset()
testset.selection_file='./resource/svincrdiscover/template/heavy.txt'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
