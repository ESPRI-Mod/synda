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
import fabric.api
from svtestutils import fabric_run

@fabric.api.task
def configure():

    # post-processing password
    fabric_run("sudo sed -i '3s|password=foobar|password=%s|' /etc/synda/sdt/credentials.conf"%(pp_password,)) # beware: line number specific

    # ESGF password
    openid='https://pcmdi.llnl.gov/esgf-idp/openid/syndatest'
    fabric_run("sudo sed -i 's|openid=https://esgf-node.ipsl.fr/esgf-idp/openid/foo|openid=%s|' /etc/synda/sdt/credentials.conf"%(openid,))
    fabric_run("sudo sed -i '7s|password=foobar|password=%s|' /etc/synda/sdt/credentials.conf"%(esgf_password,)) # beware: line number specific

@fabric.api.task
def disable_download():
    fabric_run("sudo sed -i 's|^download=true|download=false|' /etc/synda/sdt/sdt.conf")

@fabric.api.task
def restart():
    fabric_run("sudo service synda restart")

@fabric.api.task
def stop():
    fabric_run("sudo service synda stop")

@fabric.api.task
def reset():
    fabric_run("sudo rm -f /var/log/synda/sdt/*")
    fabric_run("sudo rm -f /var/lib/synda/sdt/sdt.db")

@fabric.api.task
def execute_basic_command():
    fabric_run('synda -V')

@fabric.api.task
def check_version():
    fabric_run('test %s = $( synda -V 2>&1 )'%sdt_version)

# init.
sdt_version='3.6'
pp_password='bar'
esgf_password='foo'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
