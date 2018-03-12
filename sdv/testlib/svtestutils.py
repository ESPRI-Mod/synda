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
import sys
import datetime
import argparse
import fabric.api

class SDTimer():
    @classmethod
    def get_time(cls):
        return datetime.datetime.now()

    @classmethod
    def get_elapsed_time(cls,start_time):
        """
        Returns:
            duration (in seconds)
        """
        stop_time=datetime.datetime.now()
        delt=stop_time-start_time

        return (delt.microseconds + (delt.seconds + delt.days * 24 * 3600) * 10**6) / 10**6 # microsecond is present here, but disappear after the last division. duration unit is second.

def task_exec(task):

    print
    print task.name
    print

    fabric.api.execute(task)

    print
    print

    if interactive:
        raw_input('Press any key to continue..')

def title(s):
    print '*** %s ***'%s
    print 

def fabric_run(cmd):

    if installation_mode=='source':

        cmd=cmd.replace('sudo ','')

        # SDT
        cmd=cmd.replace('service synda','synda daemon')
        cmd=cmd.replace('service sdt','synda daemon')
        cmd=cmd.replace('/etc/synda/sdt','%s/sdt/conf'%home)
        cmd=cmd.replace('/var/log/synda/sdt','%s/sdt/log'%home)
        cmd=cmd.replace('/var/lib/synda/sdt','%s/sdt/db'%home)
        cmd=cmd.replace('/usr/share/python/synda/sdt/bin','%s/sdt/lib/sd'%home)

        # SDP
        cmd=cmd.replace('service sdp','spdaemon')
        cmd=cmd.replace('/etc/synda/sdp','%s/sdp/conf'%home)
        cmd=cmd.replace('/var/log/synda/sdp','%s/sdp/log'%home)
        cmd=cmd.replace('/var/lib/synda/sdp','%s/sdp/db'%home)
        cmd=cmd.replace('/usr/share/python/synda/sdp/bin','%s/sdp/lib/sp'%home)

    elif installation_mode=='system_package':
        pass # nothing to do as this is the default

    if exec_mode=='local':
        result=fabric.api.local(cmd,shell='/bin/bash',capture=True)
    else:
        result=fabric.api.run(cmd,shell='/bin/bash')

    return result

class Testset(object):
    parameter=None
    selection_file=None

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    Args:
        - "question" is a string that is presented to the user.
        - "default" is the presumed answer if the user just hits <Enter>.

    Returns:
        - True if answer is yes
        - False if answer is no
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stderr.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stderr.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

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

# verbosity mode
#fabric.state.output['running'] = False

interactive=False

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
