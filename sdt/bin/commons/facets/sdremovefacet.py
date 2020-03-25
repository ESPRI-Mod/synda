#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""
This module remove prohibited system facets and facets with special 'all' value.
"""
from sdt.bin.commons.utils import sdconst


def run(facets_groups):
    facets_groups_new = []

    for facets_group in facets_groups:
        facets_group = process_wildcard(facets_group)
        facets_group = remove_system_facets(facets_group)

        facets_groups_new.append(facets_group)

    return facets_groups_new


def process_wildcard(facets_group):
    """Process "*" and "all" special values."""

    # The tricky code below is because dict objet can't be
    # modified on the fly.

    keys_to_remove = []
    for k, values in facets_group.items():
        if len(values) == 1:
            value = values[0]
            if value in ("all", "*"):
                keys_to_remove.append(k)

    for k in keys_to_remove:
        try:
            del facets_group[k]
        except KeyError:
            pass

    return facets_group


def remove_system_facets(facets_group):
    # This is in case user set those parameters in selection file. Those
    # parameters should not be set by user, as they are set automatically by
    # Synda ('fields' and 'format' are set in sdremoteqbuilder.py,
    # 'facets' is used in sdremoteparam, 'offset' is set in 'Request' class).

    for k in sdconst.SANAP:
        if k in facets_group:
            del facets_group[k]

    return facets_group
