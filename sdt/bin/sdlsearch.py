#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module search files in local SQL database.

Note
    sdlsearch mean 'SynDa Local Search'
"""

import os
import argparse
import sdapp
import sdpipeline
import sdutils
import sdi18n
import sdcliex
import sddb
import humanize
import sdsqlutils
import sddquery
import sdprint
from sdtypes import File,Dataset

def run(stream=None,path=None,parameter=None,dry_run=False,load_default=None):

    if parameter is None:
        parameter=[]

    queries=sdpipeline.build_queries(stream=stream,path=path,parameter=parameter,query_type='local',dry_run=dry_run,load_default=load_default)

    files=[]
    for query in queries:
        sqlquery=query['sqlquery']
        ap=query['attached_parameters']
        type_=sddquery.get_scalar(ap,'type') # yes, get_scalar works also on attached_parameters

        if dry_run:
            print sqlquery
        else:
            files.extend(get_files(sqlquery,type_))

    return files

def get_files(q,type_,conn=sddb.conn):
    files=[]

    c = conn.cursor()
    c.execute(q)
    rs=c.fetchone()
    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,eval(type_))) # HACK: improve this
        rs=c.fetchone()
    c.close()

    return files

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""examples of use
  %s -f file
  cat file | %s
%s
"""%(prog,prog,sdcliex.search(prog)))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    parser.add_argument('-c','--count',action='store_true',help='Count how many files are found')
    parser.add_argument('-f','--file',default=None)
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()

    files=run(path=args.file,parameter=args.parameter,dry_run=args.dry_run,load_default=None)

    if not args.dry_run:
        if args.count:
            print "%i"%len(files)
        else:
            for f in files:
                print "%-9s %-8s %s"%(f.status,humanize.naturalsize(f.size,gnu=False),f.file_functional_id)
