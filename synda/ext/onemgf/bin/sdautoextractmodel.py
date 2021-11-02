#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module extracts model from identifier.

Note
    This module works together with the 'sdonemgf_pre' module.
"""

from synda.sdt import sdextractitem
from synda.source.config.file.user.preferences.models import Config as Preferences


def run(facets_groups):

    onemgf = Preferences().is_behaviour_onemgf
    if onemgf:
        facets_groups = sdextractitem.run(facets_groups, 'model')

    return facets_groups
