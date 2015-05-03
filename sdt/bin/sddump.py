#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module dumps data in bulk mode.

Example of use
    sddump.py type=Dataset searchapi_host=esgf-data.dkrz.de -a timestamp
"""

import argparse
import sdapp
import sdprint
import sdsearch

def run():
    pass

def dump_ESGF(parameter,attribute,dry_run=False):
    """This func dumps attribute for all ESGF matching files/datasets.

    Initially designed to batch update attribute in Synchro-data
    (e.g. when a new attribute is decided to be stored in Synchro-data,
    all already downloaded files metadata must be updated).
    """

    parameter.append("fields=instance_id,%s"%attribute)
    parameter.append("replica=false")

    files=sdsearch.run(parameter=parameter,post_pipeline_mode=None,dry_run=dry_run)
    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('parameter',nargs='*',default=[])

    parser.add_argument('-a','--attribute',required=True)
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()

    files=dump_ESGF(args.parameter,args.attribute,dry_run=args.dry_run)

    if not args.dry_run:
        sdprint.print_format(files,args.format)
