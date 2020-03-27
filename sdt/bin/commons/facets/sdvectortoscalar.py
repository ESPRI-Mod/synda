#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module transform list type to scalar type for some facets."""

from sdt.bin.commons.utils import sdconst


def run(facets_groups):
    facets_groups_new = []

    for facets_group in facets_groups:
        facets_group = transform_parameters_type(facets_group)
        facets_groups_new.append(facets_group)

    return facets_groups_new


def transform_parameters_type(facets_group):
    """Fix parameters type.

    In the beginning of the process, all selection parameters are set with 'list' type, even for scalar parameters.
    This function fixes this issue.
    """

    for k in sdconst.SDSSSP:
        if k in facets_group:
            facets_group[k] = facets_group[k][0]

    return facets_group
