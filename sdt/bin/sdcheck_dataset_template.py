#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script checks if there is a match between dataset_functional_id and dataset template filled with facets values."""

import os
import sys
import re
import argparse
import json
import sdapp
from sdexception import SDException
import sdlog
import sdprint

def run(files):
    check_DRS_consistency(files)
    return files

def check_DRS_consistency(files):

    def remove_version_from_path(dataset_functional_id):
        """
        BEWARE: we expect in this func that the last field of the "dataset_functional_id" is
                the dataset version, no matter what the project is.
        """
        return re.sub('\.[^.]+$','',dataset_functional_id) # remove last field (version)

    for f in files:
        if "dataset_template" in f: # For some project, template is missing. In this case, we don"t do the check.

            # TODO: maybe replace '.' with '/' character in code below (i.e. misleading because variables below are called path, but do not contain '/')

            path_from_id=remove_version_from_path(f["dataset_functional_id"])
            path_from_template=f["dataset_template"]%f

            if path_from_id!=path_from_template:
                sdlog.warning("SDCHKFIL-001","inconsistency detected between metadata and search-API facet (path_from_id=%s,path_from_template=%s)"%(path_from_id,path_from_template))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
