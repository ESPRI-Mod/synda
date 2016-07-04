#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains type insensitive action used by 'synda' script.

Note
    In this file, module import directives are moved near the calls,
    so to improve startup time.
"""

import sys
from sptools import print_stderr
import spexception

def daemon(args):
    import spdaemon,spconfig

    if args.action is None:
        spdaemon.print_daemon_status()
    else:

        if args.action in ['start','stop']:
            if spconfig.system_pkg_install:
                print_stderr("Daemon must be managed using 'service' command (system package installation)")
                return 1

        if args.action=="start":

            if spdaemon.is_running():
                print_stderr("Daemon already started")
            else:
                try:
                    spdaemon.start()
                    print_stderr("Daemon successfully started")
                except spexception.SPException,e:
                    print_stderr('error occured',e.msg)
        elif args.action=="stop":

            if spdaemon.is_running():
                try:
                    spdaemon.stop()
                    print_stderr("Daemon successfully stopped")
                except spexception.SPException,e:
                    print_stderr('error occured',e.msg)
            else:
                print_stderr("Daemon already stopped")
        elif args.action=="status":
            spdaemon.print_daemon_status()

def queue(args):
    import spstatquery
    #from tabulate import tabulate

    di=spstatquery.get_ppprun_stat()

    for project in di:
        print project
        for status in di[project]:
            print '%10s: %3d'%(status,di[project][status])

    #print tabulate(li,headers=['project','status','count'],tablefmt="plain")

# init.

subcommands={
    'daemon':daemon, 
    'queue':queue
}
