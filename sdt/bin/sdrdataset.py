#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains *remote* dataset search and display routines."""

import os
import argparse
import sdapp
import sdquicksearch
from tabulate import tabulate
from sdtools import print_stderr
import sdi18n
import sdcliex
import sddeferredbefore
import humanize

def get_datasets(stream=None,parameter=None,post_pipeline_mode='dataset',dry_run=False): # TODO: maybe remove parameter argument everywhere as there is a mess in get_selection_file_buffer, because of default/forced parameter (i.e. len(parameter) is non-zero even if non parameter args set on CLI !)

    if parameter is None:
        parameter=[]

    assert (stream is None) or (len(parameter)<1) # this is to prevent using stream and parameter together
    assert post_pipeline_mode!='file'

    if len(parameter)>0:
        sddeferredbefore.add_forced_parameter(parameter,'type','Dataset')
    elif stream is not None:
        sddeferredbefore.add_forced_parameter(stream,'type','Dataset')

    result=sdquicksearch.run(stream=stream,parameter=parameter,post_pipeline_mode=post_pipeline_mode,dry_run=dry_run)
    return result.get_files()

def get_dataset(stream=None,parameter=None,dry_run=False):

    if parameter is None:
        parameter=[]

    datasets=get_datasets(stream=stream,parameter=parameter,dry_run=dry_run)
    if len(datasets)==0:
        d=None
    else:
        d=datasets[0]

        # retrieve dataset's files TAG54H4JK5H4J5
        """
        dataset_functional_id=d['dataset_functional_id']
        d.files=sdquicksearch.run(parameter=['type=File','dataset_id=%s'%dataset_functional_id],post_pipeline_mode='file',dry_run=False)
        """

    return d

def print_replica_list(datasets):
    """Print dataset list in a multi-replica context."""
    li=[[d['status'],d['dataset_functional_id'],d['data_node']] for d in datasets]
    print tabulate(li,tablefmt="plain")

def print_list(datasets):
    """Print dataset list in a mono-replica context."""
    li=[[d['status'],d['dataset_functional_id']] for d in datasets]
    print tabulate(li,tablefmt="plain")

def print_details(d,verbose=False):
    print "Dataset: %s"%d['dataset_functional_id']
    print "Datanode: %s"%d['data_node']

    if verbose:
        print "ESGF identifier (id): %s|%s"%(d['dataset_functional_id'],d['data_node'])

    print "Dataset total size: %s"%humanize.naturalsize(int(d['size']),gnu=False)
    print "Dataset variable(s) list: %s"%','.join(d['variable'])

    if verbose:

        """
        Disabled for now as not ready yet (see TAG54H4JK5H4J5)

        Maybe completely remove files listing here as it seems to be more
        ergonomic not to group datasets and files listing together (when user
        wants datasets listing, he ask for it, when he wants files listing he
        ask for it with a new request). TBC.
        """

        """
        print
        print "Dataset files list:"
        for f in d.files:
            print "%-15s  %s"%(f['size'],f['filename'])
        print "%i files found."%(len(d.files),)
        """

        pass

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use
%s
"""%sdcliex.search(prog))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()

    datasets=get_datasets(parameter=args.parameter,dry_run=args.dry_run)
    if not args.dry_run:
        print_list(datasets)
