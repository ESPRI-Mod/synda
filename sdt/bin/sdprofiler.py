#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains profiling functions."""

from sdtime import SDTimer
import sdlog
import sdconfig

def timeit(func=None):
    """This is a decorator used to time a func."""

    if sdconfig.config.get('log','scheduler_profiling')=='1':
        def inner(*args,**kwargs):

            start_time=SDTimer.get_time()
            result = func(*args,**kwargs)
            elapsed_time=SDTimer.get_elapsed_time(start_time)

            sdlog.info('SDPROFIL-001','%s ran in %2.9f sec' %(func.__name__,elapsed_time))

            return result

        return inner
    else:
        return func
