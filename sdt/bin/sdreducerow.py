#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdreducerow.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script remove incomplete/malformed files.

Description
    This module contains file rejection step 2 (file rejection step 1 is done
    by sdpostxptransform module).
"""

import sys
import argparse
import json
import sdapp
import sdlog
import sdprint

def run(files):
    files=remove_incomplete_files(files)
    #files=remove_malformed_files(files)
    return files 

def is_file_complete(file):
    filename=file.get("title")

    if file.get("dataset_id") is None:
        sdlog.error("SDREDUCE-002","incorrect dataset_id (filename=%s)"%filename)
        return False

    if file.get("url") is None:
        sdlog.error("SDREDUCE-001","incorrect url (%s)"%filename)
        return False

    """
    if file.get("tracking_id") is None:
        sdlog.log("SDREDUCE-010","incorrect tracking_id (%s)"%filename)
        return False
    """

    return True

def remove_incomplete_files(files):
    new_files=[]
    for f in files:
        if is_file_complete(f):
            new_files.append(f)

    return new_files

"""
def is_file_malformed(file):
    variable=file.get("variable")

    print type(variable)

    return False

def remove_malformed_files(files):
    new_files=[]
    for f in files:
        if is_file_malformed(f):
            pass
        else:
            new_files.append(f)

    return new_files
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
