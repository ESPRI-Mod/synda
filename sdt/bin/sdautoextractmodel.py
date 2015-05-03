#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

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

import sdextractitem
import sdconfig

def run(facets_groups):

    onemgf=sdconfig.config.getboolean('behaviour','onemgf')
    if onemgf:
        facets_groups=sdextractitem.run(facets_groups,'model')

    return facets_groups
