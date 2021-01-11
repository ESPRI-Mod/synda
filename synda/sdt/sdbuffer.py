#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains buffer building function."""

import os
import sys
import sdapp
import sdselectionfileutils
import sdtools
from sdtypes import Buffer
from sdexception import SDException, FileNotFoundException

from synda.source.config.input.constants import USER_INPUT_TYPES


def get_selection_file_buffer(path=None, parameter=None):
    """Retrieve input facets from file, stdin or command line argument and returns a Buffer object.

    Args:
        path: selection file path
        parameter: facets from command line arguments
    """

    if parameter is None:
        parameter = []

    # coherence check
    if path is not None and len(parameter) > 0:
        # both file and parameter, raise exception
        raise SDException(
            "SDBUFFER-001",
            "Incorrect arguments (path=%s, parameter=%s)" % (path, parameter),
        )

    # mode decision
    if path is not None:
        if path == "-":
            mode = 'stdin'
        else:
            mode = 'file'
    else:
        if len(parameter) > 0:
            # note that we can't restrict this test for when len(parameter)==1
            # because some system parameter are added to the list (e.g. add_forced_parameter() in 'sdrfile' module)
            if '-' in parameter:
                # deprecated case: remove this case, as we don't use it anymore
                # (i.e. it's the same result for both branch)

                # mode='stdin'
                mode = 'parameter'
            else:
                mode = 'parameter'
        else:
            import select
            if select.select([sys.stdin, ], [], [], 0.0)[0]:
                mode = 'stdin'
            else:
                mode = 'parameter'

    # perform mode specific routine

    _buffer = None
    if mode == 'parameter':

        _buffer = Buffer(
            path=USER_INPUT_TYPES["cmdline"],
            filename=USER_INPUT_TYPES["cmdline"],
            lines=parameter,
        )

    elif mode == 'stdin':

        lines = sys.stdin.readlines()

        if len(lines) == 1:
            # assume all parameter are on one line with space acting as facet delimiter (i.e. not as value delimiter)

            parameter = lines[0].split()
            _buffer = Buffer(
                path=USER_INPUT_TYPES["stdin"],
                filename=USER_INPUT_TYPES["stdin"],
                lines=parameter,
            )
        else:
            # assume same exact format as selection file

            # remove newline
            lines = [sdtools.portable_chomp(line) for line in lines]
            _buffer = Buffer(
                path=USER_INPUT_TYPES["stdin"],
                filename=USER_INPUT_TYPES["stdin"],
                lines=lines,
            )

    elif mode == 'file':
        path = sdselectionfileutils.find_selection_file(path)

        if not os.path.isfile(path):
            raise FileNotFoundException(
                'SDBUFFER-002',
                'File not found (%s)' % path,
            )

        with open(path, 'r') as fh:

            lines = fh.readlines()
            # remove newline
            lines = [sdtools.portable_chomp(line) for line in lines]

            _buffer = Buffer(
                path=path,
                filename=os.path.basename(path),
                lines=lines,
            )

    return _buffer
