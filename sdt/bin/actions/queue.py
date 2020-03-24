#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from tabulate import tabulate

from sdt.bin.db import session
from sdt.bin.db import dao
from sdt.bin.commons.utils.sdprogress import ProgressThread


def run(args):
    with session.create():
        ProgressThread.start(sleep=0.1, running_message='Collecting status information.. ', end_message='')
        li = dao.get_download_status(project=args.project)
        ProgressThread.stop()  # spinner stop

        print(tabulate(li, headers=['status', 'count', 'size'], tablefmt="plain"))
        # sddaemon.print_daemon_status()
