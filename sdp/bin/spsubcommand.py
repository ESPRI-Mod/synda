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
from sdtools import print_stderr
import sdexception

def daemon(args):
    import sddaemon,sdconfig

    if args.action is None:
        sddaemon.print_daemon_status()
    else:

        if args.action in ['start','stop']:
            if sdconfig.multiuser:
                print_stderr("When synda is installed with system package, daemon must be managed using 'service' command")
                return 1

        if args.action=="start":

            if sddaemon.is_running():
                print_stderr("Daemon already started")
            else:
                try:
                    sddaemon.start()
                    print_stderr("Daemon successfully started")
                except sdexception.SDException,e:
                    print_stderr('error occured',e.msg)
        elif args.action=="stop":

            if sddaemon.is_running():
                try:
                    sddaemon.stop()
                    print_stderr("Daemon successfully stopped")
                except sdexception.SDException,e:
                    print_stderr('error occured',e.msg)
            else:
                print_stderr("Daemon already stopped")
        elif args.action=="status":
            sddaemon.print_daemon_status()

def queue(args):
    import sdfilequery
    from tabulate import tabulate
    from sdprogress import ProgressThread

    ProgressThread.start(sleep=0.1,running_message='Collecting status information.. ',end_message='') # spinner start
    li=sdfilequery.get_download_status(args.project)
    ProgressThread.stop() # spinner stop

    print tabulate(li,headers=['status','count','size'],tablefmt="plain")
    #sddaemon.print_daemon_status()

# init.

subcommands={
    'daemon':daemon, 
    'queue':queue
}
