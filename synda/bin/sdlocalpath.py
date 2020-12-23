#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module compute local path for both file and dataset."""

import sys
import argparse
import json
import sdapp
import sdprint
import sdlocalpathtransform
import sdlocalpathutils

def run(files,mode='file'):

    # set dataset localpath keyname
    if mode=='file':
        dataset_localpath_keyname="dataset_local_path"
    elif mode=='dataset':
        dataset_localpath_keyname="local_path"
    else:
        assert False

    # warning: dot not change blocks order below

    # add dataset localpath attribute
    files=add_dataset_local_path(files,dataset_localpath_keyname)

    # add file localpath attribute
    if mode=='file':
        files=add_file_local_path(files)

    return files

def add_dataset_local_path(files,key):
    for f in files:
        f[key]=sdlocalpathutils.build_dataset_local_path(f)

    files=sdlocalpathtransform.transform_local_path_product(files,key)
    files=sdlocalpathtransform.transform_local_path_project(files,key)

    return files

def add_file_local_path(files):
    for f in files:
        f["local_path"]=sdlocalpathutils.build_file_local_path(f)

    return files

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    files=run(files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
