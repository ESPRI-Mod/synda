#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.bin.commons.utils import sdmodify
from sdt.bin.commons.utils.sdprint import print_stderr


def run(args):
    """
    Marks files that went into error for retry
    """

    nbr = sdmodify.retry_all()
    if nbr > 0:
        print_stderr("{} file(s) marked for retry.".format(nbr))
    else:
        print_stderr("No transfer in error")
