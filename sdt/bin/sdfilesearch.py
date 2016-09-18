#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains file search routines (one for each 'metadata_server_type')."""

from sdtools import print_stderr

def esgf_search_api(args):
    import sdrfile, sddeferredafter

    # tuning: note that we don't reduce the number of field returned here.
    # Maybe change that to optimise download time / reduce bandwidth footprint.

    sddeferredafter.add_default_parameter(args.stream,'limit',args.limit)

    files=sdrfile.get_files(stream=args.stream,dry_run=args.dry_run)

    if not args.dry_run:
        if len(files)==0:
            print_stderr("File not found")   
        else:
            if args.replica:
                sdrfile.print_replica_list(files)
            else:
                sdrfile.print_list(files)

def apache_default_listing(args):
    import sdearlystreamutils, sdhtmlbasic

    urls=sdearlystreamutils.get_facet_values_early(args.stream,'url')
    if len(urls)==0:
        # no url in stream

        print_stderr("Incorrect argument: please specify an url")
        return 1
    else:
        files=sdhtmlbasic.get_files(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if len(files)==0:
                print_stderr("File not found")   
            else:
                sdhtmlbasic.print_list(files)

def thredds_catalog(args):
    print_stderr("Not implemented")
    return 1
