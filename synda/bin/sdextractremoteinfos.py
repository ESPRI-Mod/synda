#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module extract informations from ESGF archive such as datasets with small size, large files, etc.."""

import argparse
import humanize
import sdapp
import sdquicksearch
import sdsample
import sdtools

def print_small_dataset(project,sample_size=2000):
    """This func retrieves a bunch of datasets and returns the smallest (not the smallest of the project, just of the subset)."""

    result=sdsample.get_sample_datasets(project,sample_size)
    if result.count()>0:

        files=result.get_files()

        # str to int
        for d in files:
            if 'size' not in d:
                print "'size' attribute missing for '%s' project"%project
                print

                return # stops processing this project
            else:
                d['size']=int(d['size'])

        # find the smallest
        smallest_size=files[0]['size'] # arbitrary
        smallest=files[0]              # arbitrary
        for d in files:
            if d['size']<smallest_size:
               smallest=d

        print "%s" % project
        print "%s" % smallest['dataset_functional_id']
        print "%s" % humanize.naturalsize(smallest['size'],gnu=False)
        print

def get_sorted_files(project,sample_size,sort_key='size'):
    result=sdsample.get_sample_files(project,sample_size)
    if result.count()>0:

        files=result.get_files()

        # cast str to int
        for f in files:
            if sort_key not in f:
                print "'%s' attribute missing for '%s' project"%(sort_key,project)
                print

                return # stops processing this project
            else:
                f[sort_key]=int(f[sort_key])

        # sort
        files=sorted(files, key=lambda x: x[sort_key])

        return files

    else:
        return []

def print_files(file_):
    print "%s" % file_['project']
    print "%s" % file_['file_functional_id']
    print "%s" % humanize.naturalsize(file_['size'],gnu=False)
    print

def print_small_files(project,sample_size=2000):
    """This func retrieves a bunch of files and returns the smallest (not the
    smallest of the project, just of the subset).
    """

    files=get_sorted_files(project,sample_size)

    # print the 10 smallest
    for file_ in files[:10]:
        print_files(file_)

def print_large_files(project,sample_size=2000):
    """This func retrieves a bunch of files and returns the largest (not the
    largest of the project, just of the subset).
    """

    files=get_sorted_files(project,sample_size)

    # print the 10 largest
    for file_ in files[-10:]:
        print_files(file_)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--action',choices=['small','large'],default='small')
    parser.add_argument('-d','--dataset',action='store_true',help='Print datasets sample')
    parser.add_argument('-f','--file',action='store_true',help='Print files sample')
    parser.add_argument('-p','--project',default='CMIP5')
    parser.add_argument('-s','--sample_size',default=2000)
    args = parser.parse_args()

    if args.action=='small':
        if args.dataset:
            print_small_dataset(args.project,args.sample_size)
        elif args.file:
            print_small_files(args.project,args.sample_size)
    elif args.action=='large':
        if args.dataset:
            sdtools.print_stderr('Not implemented')
        elif args.file:
            print_large_files(args.project,args.sample_size)
