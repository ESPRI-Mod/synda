#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module keeps files in the given timeslice range."""

import sys
import re
import argparse
import json
import sdapp
from sdtypes import File
from sdexception import SDException
import sdprint
import sdpostpipelineutils

def run(files):
    new_files=[]
    for file in files:
        allowed_time_ranges=sdpostpipelineutils.get_attached_parameter(file,'timeslice')

        if allowed_time_ranges is None:
            new_files.append(file)
        else:
            file_timeslice=get_timeslice_from_filename(file['title'])

            if timeslice_in_allowed_time_range(file_timeslice,allowed_time_ranges):
                new_files.append(file)
            else:
                pass

    return new_files

def timeslice_in_allowed_time_range(file_timeslice,allowed_time_ranges):
    for allowed_time_range in allowed_time_ranges:
        (start,stop)=split_timeslice(file_timeslice)
        (allowed_range_start,allowed_range_stop)=split_timeslice(allowed_time_range)

        if (allowed_range_start<=start) and (allowed_range_stop>=stop):
            return True
        else:
            continue

    return False

def split_timeslice(timeslice):
    (start,end)=timeslice.split('-')


    # For now, supported granularity for timeslice is YYYYMM (year and month).
    # So we remove here finer grained timestamp info if any (i.e. day,hour,etc..).
    # Finer grained timestamp info exists for example in 3hr file (i.e. frequency=3hr).
    #
    start=start[0:6]
    end=end[0:6]

    return (start,end)

def get_timeslice_from_filename(filename):
    # samples input
    #  non-FX case 1: sfcWind_Amon_CNRM-CM5_1pctCO2_r1i1p1_195001-198912.nc
    #  non-FX case 2: sfcWind_Amon_CNRM-CM5_1pctCO2_r1i1p1_195001-198912.nc_0
    #  non-FX case 3: pr_TRMM-L3_v7_201209010130-201209302230.nc
    #  FX case:       sfcWind_Amon_CNRM-CM5_1pctCO2_r1i1p1.nc
    # samples output
    #  195001-198912

    timeslice=None
    m=re.search('_([^_]+)\.nc.*$',filename)
    if(m!=None):
        timeslice=m.group(1)
    else:
        raise SDException("SDTIMSLI-001","incorrect filename (%s)"%filename)

    return timeslice

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    files=run(files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
