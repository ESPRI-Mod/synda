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

import os
import argparse
import fabric.api

def fabric_run(cmd):

    if installation_mode=='source':
        cmd=cmd.replace('sudo service synda','synda daemon')
        cmd=cmd.replace('sudo ','')
        cmd=cmd.replace('/etc/synda/sdt','%s/sdt/conf'%home)
        cmd=cmd.replace('/var/log/synda/sdt','%s/sdt/log'%home)
        cmd=cmd.replace('/var/lib/synda/sdt','%s/sdt/db'%home)

    elif installation_mode=='system_package':
        pass # nothing to do as this is the default

    if exec_mode=='local':
        fabric.api.local(cmd)
    else:
        fabric.api.run(cmd)

# init.
exec_mode='local'
installation_mode='source'
#installation_mode='system_package'

normal_user='foobar' # not used
home=os.environ['HOME']

# fabric init.
#fabric.api.env.hosts = ['myserver']
#fabric.api.env.key_filename = v.keyfile()
#fabric.api.env.disable_known_hosts = True

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()