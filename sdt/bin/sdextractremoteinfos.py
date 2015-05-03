#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module provides informations regarding ESGF archive."""

import argparse
import humanize
import sdapp
import sdquicksearch
import sdsample

def print_small_dataset(project,sample_size=2000):
    """This func retrieves a bunch of datasets and returns the smallest (not the smallest of the project, just of the subset)."""

    result=sdsample.get_sample_datasets(project,sample_size)
    if result.num_result>0:

        files=result.files

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
        print "%s" % smallest['id']
        print "%s" % humanize.naturalsize(smallest['size'],gnu=False)
        print

def print_small_files(project,sample_size=2000):
    """This func retrieves a bunch of files and returns the smallest (not the smallest of the project, just of the subset)."""

    result=sdsample.get_sample_files(project,sample_size)
    if result.num_result>0:

        files=result.files

        # cast str to int
        for f in files:
            if 'size' not in f:
                print "'size' attribute missing for '%s' project"%project
                print

                return # stops processing this project
            else:
                f['size']=int(f['size'])

        # sort
        files=sorted(files, key=lambda x: x['size'])

        # print the 10 smallest
        for i in range(10):
            file=files[i]

            print "%s" % project
            print "%s" % file['id']
            print "%s" % humanize.naturalsize(file['size'],gnu=False)
            print

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dataset',action='store_true',help='Print small datasets sample')
    parser.add_argument('-f','--file',action='store_true',help='Print small files sample')
    parser.add_argument('-p','--project',default='CMIP5')
    args = parser.parse_args()

    if args.dataset:
        print_small_dataset(args.project)
    elif args.file:
        print_small_files(args.project)
