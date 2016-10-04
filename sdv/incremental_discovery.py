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

import argparse
import re
import time
import fabric.api
from testcommon import fabric_run

def run():

    # fabric init.
    #fabric.api.env.hosts = ['myserver']
    #fabric.api.env.key_filename = v.keyfile()
    #fabric.api.env.disable_known_hosts = True

    @fabric.api.task
    def configure_task():

        # post-processing password
        fabric_run("sudo sed -i '3s|password=foobar|password=%s|' /etc/synda/sdt/credentials.conf"%(pp_password,)) # beware: line number specific

        # ESGF password
        openid='https://pcmdi.llnl.gov/esgf-idp/openid/syndatest'
        fabric_run("sudo sed -i 's|openid=https://esgf-node.ipsl.fr/esgf-idp/openid/foo|openid=%s|' /etc/synda/sdt/credentials.conf"%(openid,))
        fabric_run("sudo sed -i '7s|password=foobar|password=%s|' /etc/synda/sdt/credentials.conf"%(esgf_password,)) # beware: line number specific

    @fabric.api.task
    def restart():
        fabric_run("sudo service synda restart")

    @fabric.api.task
    def stop():
        fabric_run("sudo service synda stop")

    @fabric.api.task
    def execute_basic_command():
        fabric_run('synda -V')

    @fabric.api.task
    def check_version():
        fabric_run('test %s = $( synda -V 2>&1 )'%sdt_version)

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


    fabric.api.execute(stop) 
    fabric.api.execute(configure_task) 
    fabric.api.execute(execute_basic_command)
    fabric.api.execute(check_version)

    fabric.api.execute(normal_discovery)
    fabric.api.execute(check_normal_discovery_result)
    #time.sleep(150) # give some time for the file to be downloaded (default 300)

# init.
sdt_version='3.6'
pp_password='bar'
esgf_password='foo'

exec_mode='local'
installation_mode='source'
normal_user='foobar'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
