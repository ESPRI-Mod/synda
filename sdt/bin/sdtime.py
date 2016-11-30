#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains time functions."""

import argparse
import re
import time
import datetime

def compute_duration(start_date,end_date):
    """
    Returns:
        duration (int): transfer duration in seconds

    Note: 
        This method returns 1 second as the smallest value
        (even if transfer takes less than 1 second).
    """
    if (start_date==None) or (end_date==None):
        return 1
    else:
        duration=compute_time_delta(start_date,end_date)

        if duration==0:
            return 1
        else:
            return duration

def search_api_datetime_format_to_sqlite_datetime_format(s):
    """
    Input format example: 2016-11-12T15:59:15Z
    Output format example: 2016-11-12 15:59:15.981983
    """
    s=re.sub('Z$','.888888',s) # arbitrary
    return s.replace('T',' ')

def sqlite_datetime_format_to_search_api_datetime_format(s):
    """
    Input format example: 2016-11-12 15:59:15.981983
    Output format example: 2016-11-12T15:59:15Z
    """
    if len(s)==26:
        s=re.sub('\.[^.]+$','Z',s)

    return s.replace(' ','T')

def substract_hour(s,count):
    """
    Input format example: 2016-11-12 15:59:15.981983
    """
    format = '%Y-%m-%d %H:%M:%S.%f'
    dt=datetime.datetime.strptime(s,format) - datetime.timedelta(hours=count)
    return datetime_to_isoformat_FIXED(dt)

def datetime_to_isoformat_FIXED(dt):
    """
    Original datetime isoformat method returns
        - A) YYYY-MM-DDTHH:MM:SS.mmmmmm if microsecond is not 0
        - B) YYYY-MM-DDTHH:MM:SS        if microsecond is 0

    This func fixes this issue and always returns A format
    """
    s=dt.isoformat(" ")
    s=s if len(s)==26 else s+'.000000'
    return s

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

    # hack: the idea here is to loop until microsecond is non-zero (because when it is zero, the format changes !!!)
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
        """
        Returns:
            duration (in seconds)
        """
        stop_time=datetime.datetime.now()
        delt=stop_time-start_time

        return (delt.microseconds + (delt.seconds + delt.days * 24 * 3600) * 10**6) / 10**6 # microsecond is present here, but disappear after the last division. duration unit is second.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start_time',help='2011-08-19 11:19:29.675221')
    parser.add_argument('end_time',help=now())
    args = parser.parse_args()

    print "Start: %s"%args.start_time
    print "End: %s"%args.end_time
    print "Interval: %i"%compute_time_delta(args.start_time,args.end_time)
