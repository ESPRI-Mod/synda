#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains routines to print local and remote metadata samples."""

import sdapp
import sddao
import sdfiledao
import sdsamplequery
import argparse
import sdparam
import sdquicksearch
import sdindex
import sdnetutils
from sdtypes import Request

def call_searchapi_light(host=sdindex.get_default_index(),project=None,query=None,dry_run=None):
    """Return one sample file with all attributes."""

    project_filter='' if project is None else "&project=%s"%project
    query_filter='' if query is None else "&query=%s"%query
    url='http://%s/esg-search/search?limit=1%s%s&type=File&fields=*'%(host,project_filter,query_filter)

    if dry_run:
        print url
    else:

        # FIXME: replace this func with SearchAPIProxy
        # or replace each call with this => files=sdrfile.get_files(stream=stream,post_pipeline_mode='file',dry_run=args.dry_run)
        request=Request(url=url,pagination=False)
        result=sdnetutils.call_web_service(request,60) # return Response object

        return result.files

def get_dataset_id_samples():
    return [
        'cmip5.output1.CMCC.CMCC-CM.decadal2005.mon.atmos.Amon.r1i1p1.v20120604',
        'CMIP5.output1.BCC.bcc-csm1-1.past1000.day.ocean.day.r1i1p1.v20120606',
        'obs4MIPs.NASA-GSFC.MODIS.mon.v1',
        'obs4MIPs.NASA-GSFC.GPCP.atmos.day.v20121003',
        'obs4MIPs.IPSL.CALIOP.day.v1',
        'euclipse.MOHC.HadGEM2-A.offamip.mon.v20130605'
    ]

def get_sample_datasets(project,limit):
    """This func retrieves a list of sample datasets for the given project."""

    result=sdquicksearch.run(parameter=['type=Dataset','project=%s'%project,"limit=%s"%limit],post_pipeline_mode=None)
    return result

def get_sample_files(project,limit):
    """This func retrieves a list of sample files for the given project."""

    result=sdquicksearch.run(parameter=['type=File','project=%s'%project,"limit=%s"%limit],post_pipeline_mode=None)
    return result

def print_local_samples():
    """Print one file of each local project."""
    files=[]
    for project in sdsamplequery.get_local_projects():
        files.extend(sdfiledao.get_files(project=project,limit=1))

    for f in files:
        print "%s" % (f.local_path)
        print "%s|%s" % (f.file_functional_id,f.data_node)
        print

def print_remote_samples():
    for project in sdparam.params['project']:
        print project
        print_remote_sample(project)

def print_remote_sample(project):
    """Print one random file of given project."""
    result=sdquicksearch.run(parameter=['project=%s'%project,"limit=1"])
    for f in result.files:
        print "%s" % (f['local_path'])
        print "%s|%s" % (f['file_functional_id'],f['data_node'])
        print

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--local_sample',action='store_true',help='Print one local sample for each project')
    parser.add_argument('-r','--remote_sample',action='store_true',help='Print one remote sample for each project')
    args = parser.parse_args()

    if args.local_sample:
        print_local_samples()
    elif args.remote_sample:
        print_remote_samples()
