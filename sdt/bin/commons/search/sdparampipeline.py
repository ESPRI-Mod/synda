#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'param' pipeline's tasks.

Notes
    - This pipeline run *before* the main search-api call.
    - This pipeline is used by sdquerypipeline
"""
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.facets import sdvct
from sdt.bin.commons.facets import sdignorecase
from sdt.bin.commons.facets import sdvectortoscalar
from sdt.bin.commons.facets import sdcheckparam
from sdt.bin.commons.facets import sdvalueinputalias
from sdt.bin.commons.facets import sdremovefacet
from sdt.bin.commons.facets import sddecode

from sdt.bin.commons.param import sdinference
from sdt.bin.commons.param import sddeferredbefore
from sdt.bin.commons.param import sddeferredafter

from sdt.bin.commons.esgf import sdlocal2remote
from sdt.bin.commons.esgf import sddenormodel


def run(facets_groups):
    facets_groups = sddeferredbefore.run(facets_groups)
    facets_groups = sdignorecase.run(facets_groups)
    facets_groups = sdinference.run(facets_groups)
    facets_groups = sddeferredafter.run(facets_groups)
    facets_groups = sddecode.run(facets_groups)

    # EXT_PARAM
    #
    # load extensions here
    #
    # TODO

    facets_groups = sdlocal2remote.run(facets_groups)
    facets_groups = sdvalueinputalias.run(facets_groups)
    facets_groups = sdremovefacet.run(facets_groups)
    facets_groups = sddenormodel.run(facets_groups)
    facets_groups = sdvct.run(facets_groups)

    # only vector until this point

    facets_groups = sdvectortoscalar.run(facets_groups)

    # vector and scalar from this point

    if sdconfig.config.getint('behaviour', 'check_parameter') == 1:
        sdcheckparam.run(facets_groups)

    return facets_groups
