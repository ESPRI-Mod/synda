#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains time functions."""

import time
import datetime

def compute_duration(start_date,end_date):
    """
    Returns:
        duration (int): transfer duration in seconds

    WARNING: 
        this method returns 0 when transfer takes very short time (because we
        don't use milliseconds grained but seconds grained here..).
    """
    if (start_date==None) or (end_date==None):
        return 0
    else:
        return compute_time_delta(start_date,end_date)

def compute_time_delta(start_date,end_date):
    format = '%Y-%m-%d %H:%M:%S.%f'
    sta=datetime.datetime.strptime(start_date,format)
    sto=datetime.datetime.strptime(end_date,format)
    delt=sto-sta

    # compute how many seconds by hand, as "delt.seconds" DO NOT returns total number of seconds !!!
    #
    seconds=(delt.microseconds + (delt.seconds + delt.days * 24 * 3600) * 10**6) / 10**6 # microsecond is present here, but disappear after the last division

    return seconds

def now():
    """
    output
     current date casted as string

    example
     2011-08-19 11:19:29.675221

    note
      fix microsecond bug (http://stackoverflow.com/questions/9123057/datetime-now-sometimes-in-same-loop-change-format-and-omit-fmicroseconds)
    """

    # UGLY HACK: the idea here is to loop until microsecond is non-zero (because when it is zero, the format changes !!!)
    while True: 

        l__now=datetime.datetime.now().isoformat(" ") # isoformat returns a string representing the date and time in ISO 8601 format, YYYY-MM-DDTHH:MM:SS.mmmmmm, or, if microsecond is 0, YYYY-MM-DDTHH:MM:SS

        if len(l__now)==26: # with microseconds, length is 26. Doing this, we ensure we don't return timestamp without microsecond (see note in methods header)
            return l__now

class SDTimer():
    @classmethod
    def get_time(cls):
        return datetime.datetime.now()

    @classmethod
    def get_elapsed_time(cls,start_time):
        stop_time=datetime.datetime.now()
        delt=stop_time-start_time

        return (delt.microseconds + (delt.seconds + delt.days * 24 * 3600) * 10**6) / 10**6 # microsecond is present here, but disappear after the last division. duration unit is second.
