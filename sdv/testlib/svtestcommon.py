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
import fabric
from svtestutils import fabric_run, query_yes_no

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
def do_not_print_domain_inconsistency():
    fabric_run("sudo sed -i 's|^print_domain_inconsistency=True|print_domain_inconsistency=False|' /usr/share/python/synda/sdt/bin/sdconfig.py")

@fabric.api.task
def restart():
    fabric_run("sudo service synda restart")

@fabric.api.task
def stop():
   stop_sdt()

@fabric.api.task
def stop_sdt():
    fabric_run("sudo service sdt stop")

@fabric.api.task
def stop_sdp():
    fabric_run("sudo service sdp stop")

@fabric.api.task
def stop_sdw():
    fabric_run("sudo synda_wo stop")

@fabric.api.task
def reset():
    reset_sdt()

@fabric.api.task
def reset_all():
    reset_sdt()
    reset_sdp()
    reset_data()

@fabric.api.task
def reset_sdt():
    fabric_run("sudo rm -f /var/log/synda/sdt/*")      # reset log
    fabric_run("sudo rm -f /var/lib/synda/sdt/sdt.db") # reset DB

@fabric.api.task
def reset_sdp():
    fabric_run("sudo rm -f /var/log/synda/sdp/*")
    fabric_run("sudo rm -f /var/lib/synda/sdp/sdp.db")

@fabric.api.task
def pause():
    fabric_run('read -p "Press any key to continue.." -s -n 1 ; echo')

@fabric.api.task
def reset_data():
    fabric.state.output['running'] = False
    data_folder=fabric_run('/usr/share/python/synda/sdt/bin/sdconfig.py -n data_folder')
    fabric.state.output['running'] = True

    answer=query_yes_no('%s folder will be removed. Do you want to continue ?'%data_folder, default="no")

    if answer:
        fabric_run("sudo rm -rf %s"%data_folder)
        fabric_run("sudo mkdir -p %s"%data_folder)
    else:
        raise Exception('Test cancelled !')

@fabric.api.task
def retrieve_parameters():
    fabric_run('synda update')

@fabric.api.task
def execute_basic_command():
    execute_basic_sdt_command()

@fabric.api.task
def execute_basic_sdt_command():
    fabric_run('synda -V')

@fabric.api.task
def execute_basic_sdp_command():
    fabric_run('synda_pp -V')

@fabric.api.task
def check_version():
    check_sdt_version()

@fabric.api.task
def check_sdt_version():
    fabric_run('test %s = $( synda -V 2>&1 )'%sdt_version)

@fabric.api.task
def check_sdp_version():
    fabric_run('test %s = $( synda_pp -V 2>&1 )'%sdp_version)

# init.
sdt_version='3.6'
sdp_version='1.2'
pp_password='bar'
esgf_password='foo'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
