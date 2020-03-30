#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sdmetric, sdparam


def run(args):
    # check
    if args.groupby == 'model':
        if args.project not in sdparam.params['project']:
            print_stderr("Unknown project ({})".format((args.project)))
            return 1

    if args.metric == 'size':
        sdmetric.print_size(args.groupby, args.project, dry_run=args.dry_run)
    elif args.metric == 'rate':
        sdmetric.print_rate(args.groupby, args.project, dry_run=args.dry_run)
