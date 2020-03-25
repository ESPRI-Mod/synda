#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module translates facets names.

Note
    - this module is not exactly the reverse of the 'sdlocal2remote' module,
      (e.g. non injective because of 'time_frequency' and 'instance_id')
"""
from sdt.bin.commons.facets import sdtranslate

name_rules = {
    'title': 'filename',
    'instance_id': 'file_functional_id',
    # arbitrary choice
    # (could also be 'dataset_functional_id' as 'instance_id' is used for both file and dataset in search-API)
    'dataset_id': 'dataset_functional_id'
}


def run(facets_groups):
    facets_groups_new = []

    for facets_group in facets_groups:
        facets_group = sdtranslate.translate_name(facets_group, name_rules)
        facets_groups_new.append(facets_group)

    return facets_groups_new
