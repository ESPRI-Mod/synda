#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright€œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains profiling functions."""

from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils.sdtime import SDTimer


def timeit(func=None):
    """This is a decorator used to time a func."""

    if sdconfig.config.get('log', 'scheduler_profiling') == '1':
        def inner(*args, **kwargs):

            start_time = SDTimer.get_time()
            result = func(*args, **kwargs)
            elapsed_time = SDTimer.get_elapsed_time(start_time)
            sdlog.info('SDPROFIL-001', '{} ran in {2.9f} sec'.format(func.__name__, elapsed_time))
            return result

        return inner
    else:
        return func
