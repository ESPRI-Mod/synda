#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from sdt.bin.commons.daemon import sddaemon
from sdt.bin.commons.utils import sdconfig


def run(args):
    if args.action is None:
        sddaemon.print_daemon_status()
    else:
        if args.action == "start":

            if sddaemon.is_running():
                print_stderr("Daemon already started")
            else:
                try:
                    sddaemon.start()
                    print_stderr("Daemon successfully started")
                except sdexception.SDException as e:
                    print_stderr('error occured', e.msg)
        elif args.action == "stop":

            if sddaemon.is_running():
                try:
                    sddaemon.stop()
                    print_stderr("Daemon successfully stopped")
                except sdexception.SDException as e:
                    print_stderr('error occured', e.msg)
            else:
                print_stderr("Daemon already stopped")
        elif args.action == "status":
            sddaemon.print_daemon_status()
