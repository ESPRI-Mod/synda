#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module builds and submit search-API *parameter* query.

Reference
    - https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API
"""
from sdt.bin.commons.esgf import sddenormodel
from sdt.bin.commons.esgf import sdremoteparam_light


def run(pname=None, host=None, facets_group=None, dry_run=False):
    """
    Args:
        facets_group: if present, only parameter matching facets_group filter are returned

    Returns:
        Dict of list of 'Item' object
    """

    if facets_group is None:
        facets_group = {}

    assert isinstance(facets_group, dict)

    # denorm. model
    facets_groups = sddenormodel.run([facets_group])
    facets_group = facets_groups[0]

    params = sdremoteparam_light.run(pname=pname, host=host, facets_group=facets_group, dry_run=dry_run)

    return params
