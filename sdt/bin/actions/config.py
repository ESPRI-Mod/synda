#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from sdt.bin.commons.utils import sdconfig


def run(args):
    if args.action is None:
        sdconfig.print_()
    else:
        if args.action == 'get':
            sdconfig.print_(args.name)
        elif args.action == 'set':
            # TODO see if section can be added to the argparser arguments.
            print('Feature not implemented yet.')
