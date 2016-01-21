#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script re-process ESGF id and path to fit Synda data naming rules and
add default value for missing attributes.

Note
    This module can be used to process different metadata types (File and Dataset).
"""

import os
import sys
import re
import argparse
import json
import sdapp
from sdexception import SDException
import sdlog
import sdconst
import sdprint

def run(files):
    files=add_default_values(files)
    files=rename_dataset_attributes(files)
    files=remove_datanode_from_dataset_id(files)
    add_dataset_extra_information(files)
    return files

def add_default_values(files):
    for f in files:
        if "dataset_id_template_" not in f: # for some project, this attribute is not set
            f["dataset_id_template_"]=None
    return files

def rename_dataset_attributes(files):
    for f in files:
        if "dataset_id_template_" in f:
            f["dataset_template"]=f["dataset_id_template_"]
            del f["dataset_id_template_"]

        # the if/else block below is because this module can be used to process different metadata type (File and Dataset)
        if f["type"]==sdconst.SA_TYPE_DATASET:
            f["dataset_functional_id"]=f["id"]
            del f["id"]
        elif f["type"]==sdconst.SA_TYPE_FILE:
            f["dataset_functional_id"]=f["dataset_id"]
            del f["dataset_id"]
        else:
            raise SDException('SDPREPAR-001','Incorrect type (%s)'%f["type"])

    return files

def remove_datanode_from_dataset_id(files):
    for f in files:
        f["dataset_functional_id"]=f["dataset_functional_id"].split('|')[0]     
    return files

def add_dataset_extra_information(files):
    """
    BEWARE: we expect in this func that the last field of the "dataset_functional_id" is
            the dataset version, no matter what the project is.
    """
    for f in files:
        f["dataset_path"]=f["dataset_functional_id"].replace('.','/')

        m=re.search("^(.*)/([^/]*)$",f["dataset_path"])
        if m!=None:
            f["dataset_path_without_version"]=m.group(1)
            f["dataset_version"]=m.group(2)
        else:
            raise SDException("SDPREPAR-ERR002","incorrect dataset_functional_id (%s)"%(f["dataset_path"],))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    files=run(files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
