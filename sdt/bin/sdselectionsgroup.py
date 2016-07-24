#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module manages a selections group."""

import re
import os
import glob
import argparse
import sdapp
import sdconfig
import sdselectionsgrouputils

def load_selections():
    global selections
    selections=sdselectionsgrouputils.build_selection_list()

def print_selection_list_with_index(pattern=None):
    for i,s in enumerate(get_selection_list(filename_pattern=pattern)):
        print "%3d %s"%(i,s.filename)

def print_selection_list(pattern=None,project=None):

    if project is None:
        project=[]

    for s in get_selection_list(pattern,project=project):
        print s.filename

def get_selection_list(filename_pattern=None,project=None):

    if project is None:
        project=[]

    if selections is None:
        load_selections()

    new_selections=selections

    if filename_pattern is not None:
        new_selections=sdselectionsgrouputils.filename_filter(new_selections,filename_pattern)

    new_selections=sdselectionsgrouputils.project_filter(new_selections,project)

    return new_selections

# module init.

selections=None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--pattern')
    parser.add_argument('-P','--project',action='append',default=[])
    args = parser.parse_args()

    print_selection_list(pattern=args.pattern,project=args.project)
