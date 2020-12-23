#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains *remote* file search and display routines."""

import os
import argparse
import humanize
from tabulate import tabulate
import sdapp
import sdquicksearch
from sdtypes import File
import sdi18n
import sdcliex
import sdconst
import sddeferredbefore

def get_files(stream=None,parameter=None,post_pipeline_mode='file',dry_run=False): # TODO: maybe remove parameter argument everywhere as there is a mess in get_selection_file_buffer, because of default/forced parameter (i.e. len(parameter) is non-zero even if non parameter args set on CLI !)

    if parameter is None:
        parameter=[]

    assert (stream is None) or (len(parameter)<1) # this is to prevent using stream and parameter together

    if len(parameter)>0:
        sddeferredbefore.add_forced_parameter(parameter,'type','File')
    elif stream is not None:
        sddeferredbefore.add_forced_parameter(stream,'type','File')

    result=sdquicksearch.run(stream=stream,parameter=parameter,post_pipeline_mode=post_pipeline_mode,dry_run=dry_run)
    return result.get_files()

def get_file(stream=None,parameter=None,dry_run=False):

    if parameter is None:
        parameter=[]

    files=get_files(stream=stream,parameter=parameter,dry_run=dry_run)
    if len(files)==0:
        f=None
    else:
        f=files[0]

    return f

def print_list(files):

    # WAY 1
    li=[[f['status'],humanize.naturalsize(f['size'],gnu=False), f['file_functional_id']] for f in files]
    print tabulate(li,tablefmt="plain")

    # WAY 2
    #for f in files:
    #    print "%-9s %-8s %s"%(f.status,humanize.naturalsize(f.size,gnu=False),f.file_functional_id)

    # WAY 3
    """
    pretty_label={'done':'installed'} # this is have a listing like dpkg/apt-get
    for file in files:
        f=File(**file)
        print "%-12s %s"%(pretty_label.get(f.status,f.status),f.filename)
    """

def print_replica_list(files):
    li=[[f['file_functional_id'],f['data_node']] for f in files]
    print tabulate(li,tablefmt="plain")

def print_details(f):
    f=File(**f)

    print "file: %s"%f.file_functional_id
    print "status: %s"%f.status
    print "size: %s (%s)"%(f.size,humanize.naturalsize(f.size,gnu=False))
    print "checksum: %s"%f.checksum
    print "url: %s"%f.url

    local_path_label='local path' if f.status in (sdconst.TRANSFER_STATUS_DELETE,sdconst.TRANSFER_STATUS_DONE) else 'local path (once downloaded)'
    print "%s: %s"%(local_path_label,f.get_full_local_path())

    print "replica: %s"%f.replica
    print "data_node: %s"%f.data_node

# init.

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser( formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use
%s
"""%sdcliex.search(prog))
    parser.add_argument('parameter',nargs='+',help=sdi18n.m0001)
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()

    files=get_files(parameter=args.parameter,dry_run=args.dry_run)

    if not args.dry_run:
        print_list(files)
