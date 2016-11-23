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
import sdfields
import sdstreamutils

def run():
    pass

def dump_ESGF(parameter=None,selection_file=None,fields=None,dry_run=False,playback=None,record=None,no_default=True):
    """This func dumps fields for all ESGF matching files/datasets.

    Initially designed to batch update attribute in Synda database
    (e.g. when a new attribute is decided to be stored in Synda,
    all already downloaded files metadata must be updated).
    """

    assert fields is not None

    parameter.append("fields=%s"%fields)
    parameter.append("replica=false")

    stream=sdstreamutils.get_stream(parameter=parameter,selection_file=selection_file,no_default=no_default)

    metadata=sdsearch.run(stream=stream,post_pipeline_mode=None,dry_run=dry_run,playback=playback,record=record)
    return metadata.get_files()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('parameter',nargs='*',default=[])

    parser.add_argument('-f','--fields',default=sdfields.get_sample_fields())
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()

    files=dump_ESGF(parameter=args.parameter,fields=args.fields,dry_run=args.dry_run)

    if not args.dry_run:
        sdprint.print_format(files,args.format)
