#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.bin.commons.param import sdparam
from sdt.bin.commons.param import sdinference
from sdt.bin.commons.param import sdignorecase

from sdt.bin.commons.esgf import sdremoteparam
from sdt.bin.commons import syndautils


def run(args):
    facets_groups = syndautils.get_stream(subcommand=args.subcommand, parameter=args.parameter,
                                          selection_file=args.selection_file, no_default=True)
    facets_groups = sdignorecase.run(facets_groups)
    facets_groups = sdinference.run(facets_groups)

    # first, we check in cache so to quickly return if facet is unknown
    if sdparam.exists_parameter_name(args.facet_name):

        if len(facets_groups) == 1:
            # facet selected: retrieve parameters from ESGF

            facets_group = facets_groups[0]

            params = sdremoteparam.run(pname=args.facet_name, facets_group=facets_group, dry_run=args.dry_run)

            # TODO: func for code below
            items = params.get(args.facet_name, [])
            for item in items:
                print(item.name)
        elif len(facets_groups) > 1:
            print_stderr('Multi-queries not supported')

        else:
            # Parameter not set. In this case, we retrieve facet values list from cache.

            sdparam.main([args.facet_name])  # tricks to re-use sdparam CLI parser

    else:
        print_stderr('Unknown facet')
