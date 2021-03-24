#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains file search routines (one for each 'metadata_server_type')."""
from synda.sdt import sdrfile
from synda.sdt import sddeferredafter

from synda.sdt.sdtools import print_stderr


def esgf_search_api(args):

    # tuning: note that we don't reduce the number of field returned here.
    # Maybe change that to optimise download time / reduce bandwidth footprint.

    sddeferredafter.add_default_parameter(
        args.stream,
        'limit',
        args.limit,
    )

    files = sdrfile.get_files(stream=args.stream, dry_run=args.dry_run)

    if not args.dry_run:
        if len(files) == 0:
            print_stderr("File not found")   
        else:
            if args.replica:
                sdrfile.print_replica_list(files)
            else:
                sdrfile.print_list(files)
