#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module displays data selection (e.g. selection file) statistics.

Notes
    - This filter is intended to be chained to the file pipeline output.
    - This filter use local data and data from ESGF to compute the delta

Also see
    sdmetric
"""

import sys
import argparse
import json
import humanize
import sdapp
import sdconst
import sdstatutils
import syndautils
import sdexception
import sdpipelineprocessing

def run(args):

    try:
        metadata=syndautils.file_full_search(args)
    except sdexception.EmptySelectionException, e:
        print_stderr("You must specify at least one facet to perform this action.")
        return 1

    if args.dry_run:
        return 0


    statuses=sdstatutils.init_table()
    po=sdpipelineprocessing.ProcessingObject(sdstatutils.get_statuses,statuses)
    sdpipelineprocessing.run_pipeline(metadata,po)


    total=sdstatutils.get_total(statuses)
    print_summary(statuses,total)

    return 0

def print_summary(statuses,total,mode='line'):
    if mode=='delimited':
        print "Total size;Pending size;Local size;Total files count;Pending files count;Local files count"
        print "%s;%s;%s;%s;%s;%s"%( humanize.naturalsize(total['all']['size'],gnu=False),
                                    humanize.naturalsize(total['pending']['size'],gnu=False),
                                    humanize.naturalsize(statuses['done']['size'],gnu=False),
                                    humanize.naturalsize(statuses['new']['size'],gnu=False),
                                    total['all']['count'],
                                    total['pending']['count'],
                                    statuses['done']['count'],
                                    statuses['new']['count'])
    elif mode=='line':
        print "Total files count: %s"%total['all']['count']
        #print "Pending files count: %s"%total['pending']['count']
        for s in statuses.keys():
            count=statuses[s]['count']
            if count>0:
                print "%s files count: %s"%(s.title(),count)
        print "Total size: %s"%humanize.naturalsize(total['all']['size'],gnu=False)
        #print "Pending size: %s"%humanize.naturalsize(total['pending']['size'],gnu=False)
        for s in statuses.keys():
            size=statuses[s]['size']
            if size>0:
                print "%s files size: %s"%(s.title(),humanize.naturalsize(size,gnu=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin ) # warning: load list in memory

    run(files)
