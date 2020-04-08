#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains *local* file related routines."""

import humanize
from tabulate import tabulate
import sdlsearch
from sdt.bin.commons.search import sddeferredbefore

def get_files(stream=None,parameter=None,dry_run=False):

    if parameter is None:
        parameter=[]

    assert (stream is None) or (len(parameter)<1) # this is to prevent using stream and parameter together

    if len(parameter)>0:
        sddeferredbefore.add_forced_parameter(parameter,'type','File')
    elif stream is not None:
        sddeferredbefore.add_forced_parameter(stream,'type','File')

    files=sdlsearch.run(stream=stream,parameter=parameter,dry_run=dry_run)

    return files # returns list of File object

def get_file(stream=None,dry_run=False):
    files=get_files(stream=stream,dry_run=dry_run)
    if len(files)==1:
        f=files[0]
    else:
        f=None
    return f

def print_(files):
    if len(files)==0:
        print("File not found")
    elif len(files)==1:
        f=files[0]
        print_details(f)
    elif len(files)>1:
        li=[[f.status, f.file_functional_id] for f in files]
        print(tabulate(li,tablefmt="plain"))

def print_list(files):
    li=[[f.status, f.file_functional_id,f.data_node] for f in files]
    print(tabulate(li,tablefmt="plain"))

def print_details(f):
    print("file: %s"%f.file_functional_id)
    print("status: %s"%f.status)
    print("size: %s (%s)"%(f.size,humanize.naturalsize(f.size,gnu=False)))
    print("checksum: %s"%f.checksum)
    print("url: %s"%f.url)
    print("local path: %s"%f.get_full_local_path())
    print()
