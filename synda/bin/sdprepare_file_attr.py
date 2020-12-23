#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script rename some file attributes, set primary key and add
default value for missing attributes.

Note
    The pk set in this filter will be the one used to check if file have
    already been downloaded or not. It is specialy made so not to be replicas
    dependent (so to be able to download the file from any replicas we want
    without creating local duplicates).
"""

import os
import sys
import argparse
import json
import sdapp
import sdconfig
from sdexception import SDException
import sdprint
import sdlog
import sdconst

def run(files):
    files=rename_attributes(files)
    files=transform_id(files)
    files=add_missing_attributes(files)
    return files

def add_missing_attributes(files):

    # For some files, there is no 'tracking_id' attribute set. We have to set
    # it to NULL as this informations is needed during database insertion
    # (otherwise KeyError exception occurs).
    for f in files:
        if 'tracking_id' not in f:
            f['tracking_id']=None

    # For some files, there is no 'checksum' attribute set. We have to set it
    # to NULL as this informations is needed during database insertion
    # (otherwise KeyError exception occurs).
    for f in files:
        if 'checksum' not in f:

            if sdconfig.log_domain_inconsistency:
                sdlog.warning("SDPRFIAT-001","File have no checksum (%s)"%(f["file_functional_id"],),logger_name=sdconst.LOGGER_DOMAIN)

            f['checksum']=None
            f['checksum_type']=None

    return files

def transform_id(files):
    """This func made some changes in the file identifier as shown in the example below.
    
    OLD
     cmip5.output1.NCAR.CCSM4.historical.mon.atmos.Amon.r2i1p1.v20130425.psl_Amon_CCSM4_historical_r2i1p1_185001-200512.nc_7|tds.ucar.edu
    NEW 
     cmip5.output1.NCAR.CCSM4.historical.mon.atmos.Amon.r2i1p1.v20130425.psl_Amon_CCSM4_historical_r2i1p1_185001-200512.nc
    
    notes
        - Key name is renamed from 'id' to 'file_functional_id'
        - Those changes are needed, because this identifier will be our 'existency
          check' key, and we don't want to duplicate file when retrieving replica
          (i.e. '|tds.ucar.edu') nor we want to duplicate file when having
          different file version (i.e. '_7')
    """
    

    for f in files:
        f["file_functional_id"]="%s.%s"%(f["dataset_functional_id"],f["filename"])
        del f["id"]

    return files

def rename_attributes(files):
    for f in files:

        f["filename"]=f["title"]
        del f["title"]

    return files

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    files=run(files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
