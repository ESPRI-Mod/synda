#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sdview
import syndautils
import sdsandbox
import sdtypes
import sdconst
import sdearlystreamutils
import sdlfile
import sdrfile


# TODO Depends on GrADS
# See if avoidable

def run(args):
    stream = syndautils.get_stream(subcommand=args.subcommand, parameter=args.parameter,
                                   selection_file=args.selection_file)

    # check

    li = sdearlystreamutils.get_facet_values_early(stream, 'instance_id')  # check if 'instance_id' exists
    if len(li) == 0:
        # 'instance_id' is not found on cli

        li = sdearlystreamutils.get_facet_values_early(stream, 'title')  # check if 'title' exists
        if len(li) == 0:
            # 'title' is not found on cli

            # no identifier found, we stop the processing
            print_stderr('Please specify a file identifier (id or filename).')
            return 1

        elif len(li) > 1:
            print_stderr('Too many arguments.')
            return 1
    elif len(li) > 1:
        print_stderr('Too many arguments.')
        return 1

    # discovery

    file_ = sdlfile.get_file(stream=stream)

    if file_ is None:

        file_ = sdrfile.get_file(stream=stream)

        if file_ is None:
            print_stderr("File not found")

            return 2

    # cast

    f = sdtypes.File(**file_)

    # check if file exists locally

    if f.status == sdconst.TRANSFER_STATUS_DONE:
        file_local_path = f.get_full_local_path()
    elif sdsandbox.file_exists(f.filename):
        file_local_path = sdsandbox.get_file_path(f.filename)
    else:
        file_local_path = None

    # download (if not done already)

    if file_local_path is None:
        status = sddirectdownload.run([file_], verbosity=1)

        if status != 0:
            return 1

    # open file in external viewer

    sdview.open_(file_local_path, f.variable, args.geometry)

    return 0
