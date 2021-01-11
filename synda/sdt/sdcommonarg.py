#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains args shared across multiple modules."""

import argparse

from synda.source.config.api.esgf_search.constants import STRUCTURE as SEARCH_API_STRUCTURE


def add_playback_record_options(parser, hidden=False):
    grp = parser.add_mutually_exclusive_group(required=False)

    playback_help = 'Read metadata from FILE' if not hidden else argparse.SUPPRESS
    record_help = 'Write metadata to FILE' if not hidden else argparse.SUPPRESS

    grp.add_argument('-p', '--playback', help=playback_help, metavar='FILE')
    grp.add_argument('-r', '--record', help=record_help, metavar='FILE')


def add_type_grp(parser):

    type_grp = parser.add_mutually_exclusive_group(required=False)

    type_grp.add_argument(
        '-a',
        '--aggregation',
        dest='type_',
        action='store_const',
        const=SEARCH_API_STRUCTURE['type']['aggregation'],
    )

    type_grp.add_argument(
        '-d',
        '--dataset',
        dest='type_',
        action='store_const',
        const=SEARCH_API_STRUCTURE['type']['dataset'],
    )

    type_grp.add_argument(
        '-f',
        '--file',
        dest='type_',
        action='store_const',
        const=SEARCH_API_STRUCTURE['type']['file'],
    )

    type_grp.add_argument(
        '-v',
        '--variable',
        dest='type_',
        action='store_const',
        const=SEARCH_API_STRUCTURE['type']['aggregation'],
    )
