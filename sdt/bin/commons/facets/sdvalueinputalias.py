#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module adds aliases for some parameters values (used for transition
period, but to be removed ASAP as it's better have only one way to name values
across selections)."""

from sdt.bin.commons.facets import sdtranslate


def run(facets_groups):
    for facets_group in facets_groups:
        sdtranslate.translate_value(facets_group, value_rules)
    return facets_groups


value_rules = {
    'model': {
        'inmcm4': 'INM-CM4',
        'bcc-csm1-1': 'BCC-CSM1-1',
        'bcc-csm1-1-m': 'BCC-CSM1-1-m',
        'GFDL-CM2p1': 'GFDL-CM2-1'
    },
    'institute': {
        'CCCma': 'CCCMA'
    }
}
