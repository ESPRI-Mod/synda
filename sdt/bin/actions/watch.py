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
from sdt.bin.commons.utils import sdreport
from sdt.bin.commons.utils import sdprint


def run(args):
    if sddaemon.is_running():
        sdreport.print_running_transfers()
    else:
        sdtools.print_stderr('Daemon not running')
