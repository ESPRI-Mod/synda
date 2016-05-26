#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'sandbox' folder related routines."""

import sys
import os
import argparse
import json
import sdapp
import sdconfig

def file_exists(filename):
    path=os.path.join(sandbox_folder,filename)
    return os.path.isfile(path)

def get_file_path(filename):
    path=os.path.join(sandbox_folder,filename)
    return path

sandbox_folder=sdconfig.sandbox_folder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
