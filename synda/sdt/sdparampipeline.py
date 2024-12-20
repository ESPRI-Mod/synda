#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'param' pipeline's tasks.

Notes
    - This pipeline run *before* the main search-api call.
    - This pipeline is used by sdquerypipeline
"""

import sys
import argparse
import json
from synda.sdt import sdvectortoscalar
from synda.sdt import sdvct
from synda.sdt import sdcheckparam
from synda.sdt import sdlocal2remote
from synda.sdt import sdvalueinputalias
from synda.sdt import sddenormodel
from synda.sdt import sdremovefacet
from synda.sdt import sddecode
from synda.sdt import sdignorecase
from synda.sdt import sdinference
from synda.sdt import sddeferredbefore
from synda.sdt import sddeferredafter
from synda.sdt import sdprint

from synda.source.config.file.user.preferences.models import Config


def run(facets_groups):
    facets_groups = sddeferredbefore.run(facets_groups)
    facets_groups = sdignorecase.run(facets_groups)
    facets_groups = sdinference.run(facets_groups, show_infere_parameter_name_info_message=True)
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

    if Config().behaviour_check_parameter == 1:
        sdcheckparam.run(facets_groups)

    return facets_groups

# module init.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1', '--print_only_one_item', action='store_true')
    parser.add_argument('-F', '--format', choices=sdprint.formats, default='raw')
    args = parser.parse_args()

    facets_groups = json.load(sys.stdin)
    facets_groups = run(facets_groups)
    sdprint.print_format(facets_groups, args.format, args.print_only_one_item)
