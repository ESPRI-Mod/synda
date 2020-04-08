#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.bin.commons.utils import syndautils
from sdt.bin.commons.utils import sdremove


def run(args):
    stream = syndautils.get_stream(subcommand=args.subcommand, parameter=args.parameter,
                                   selection_file=args.selection_file, no_default=args.no_default,
                                   raise_exception_if_empty=True)
    return sdremove.run(args, stream)
