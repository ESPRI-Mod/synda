#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Denormalize model names as search-API don't understand normalized model name.

Example
    'CESM1-CAM5-1-FV2' become 'CESM1(CAM5.1,FV2)'
"""

from sdt.bin.commons.param import sdparam


def run(facets_groups):
    facets_groups_new = []

    for facets_group in facets_groups:
        facets_group = denormalize_models(facets_group)
        facets_groups_new.append(facets_group)

    return facets_groups_new


def denormalize_models(facets_group):
    if 'model' in facets_group:
        facets_group['model'] = sdparam.denormalize_models_list(facets_group['model'])

    return facets_group
