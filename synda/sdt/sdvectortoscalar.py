#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module transform list type to scalar type for some facets."""

import sys
import argparse
import json
import sdprint

from synda.source.config.file.selection.constants import SDSSSP


def run(facets_groups):
    facets_groups_new = []

    for facets_group in facets_groups:
        facets_group = transform_parameters_type(facets_group)
        facets_groups_new.append(facets_group)

    return facets_groups_new


def transform_parameters_type(facets_group):
    """Fix parameters type.

    First, all selection parameters are set with 'list' type, even for scalar parameters.
    This function fix this issue.
    """

    for k in SDSSSP:
        if k in facets_group:
            facets_group[k] = facets_group[k][0]

    return facets_group


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1', '--print_only_one_item', action='store_true')
    parser.add_argument('-F', '--format', choices=sdprint.formats, default='raw')
    args = parser.parse_args()

    facets_groups_ = json.load(sys.stdin)
    facets_groups_ = run(facets_groups_)
    sdprint.print_format(
        facets_groups_,
        args.format,
        args.print_only_one_item,
    )
