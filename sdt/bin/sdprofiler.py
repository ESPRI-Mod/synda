#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdprofiler.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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
