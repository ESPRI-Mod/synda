#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains *local* dataset routines."""

import os
import argparse
import sdapp
import sddeferredbefore
import sddao
import sdfiledao
import sddatasetdao
import sddatasetquery
import sddatasetflag
import sdlsearch
import sddatasetutils
import sdi18n
import sdcliex
import sdvariable
from tabulate import tabulate

def get_datasets(stream=None,parameter=None,dry_run=False): # TODO: maybe remove parameter argument everywhere as there is a mess in get_selection_file_buffer, because of default/forced parameter (i.e. len(parameter) is non-zero even if non parameter args set on CLI !)

    if parameter is None:
        parameter=[]

    assert (stream is None) or (len(parameter)<1) # this is to prevent using stream and parameter together

    if len(parameter)>0:
        sddeferredbefore.add_forced_parameter(parameter,'type','Dataset')
    elif stream is not None:
        sddeferredbefore.add_forced_parameter(stream,'type','Dataset')

    datasets=sdlsearch.run(stream=stream,parameter=parameter,dry_run=dry_run)

    return datasets

def get_dataset(stream=None,parameter=None,dry_run=False):

    if parameter is None:
        parameter=[]

    datasets=get_datasets(stream=stream,parameter=parameter,dry_run=dry_run)
    if len(datasets)==1:
        d=datasets[0]
        d=_get_dataset_details(d.dataset_functional_id) # get dataset from DB again with more detailed informations
    else:
        d=None
    return d

def _get_dataset_details(dataset_functional_id):
    """Helper func."""
    d=sddatasetdao.get_dataset(dataset_functional_id=dataset_functional_id)

    d.dataset_versions=sddatasetquery.get_dataset_versions(d,True) # retrieves all the versions of the dataset
    d.stats=sddatasetquery.get_dataset_stats(d) 
    d.variables=sdvariable.get_variables_progress(d)
    d.files=sdfiledao.get_dataset_files(d)

    return d

def print_list(datasets):
    li=[[d.status, d.dataset_functional_id] for d in datasets] # do not add data_node here ! (there is no data_node at dataset level in local database)
    print tabulate(li,tablefmt="plain")

def print_title(title,before_space=True):

    if before_space:
        print

    print title
    print "-"*len(title)

def print_details(d):
    print_title('Main',before_space=False)
    print "dataset: %s"%d.dataset_functional_id
    print "local path: %s"%d.get_full_local_path()
    print "status: %s"%(d.status,)
    print "latest: %s"%(str(bool(d.latest)).lower(),)
    print "number of versions: %i"%(d.dataset_versions.count(),)
    # print fresh dataset status (computed on-the-fly)
    #print "computed status: %s"%(sddatasetflag.compute_dataset_status(d),)
    #print "computed latest: %s"%(sddatasetflag.compute_latest_flag(d.dataset_versions,d),)
    print_title('Files status')
    print "done: %i"%(d.stats['count']['done'],)
    print "waiting: %i"%(d.stats['count']['waiting'],)
    print "error: %i"%(d.stats['count']['error'],)
    print_title('Dataset versions list')
    for d__v in d.dataset_versions.get_datasets():
        print "%-10s (latest=%s)"%(d__v.version,bool(d__v.latest))
    print_title('Variable status')
    for l__v in d.variables:
        print "%-15s %s"%(l__v.name,l__v.status,)
    print_title('Dataset files list')
    for t in d.files:
        print "%-100s %s"%(t.filename,t.status,)

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use
%s
"""%sdcliex.search(prog))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    parser.add_argument('-g', '--debug',action='store_true')
    args = parser.parse_args()

    datasets=get_datasets(parameter=args.parameter)
    print_list(datasets)
