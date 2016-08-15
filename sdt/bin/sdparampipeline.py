#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

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
import sdapp
import sdvectortoscalar
import sdvct
import sdcheckparam
import sdlocal2remote
import sdvalueinputalias
import sddenormodel
import sdremovefacet
import sddecode
import sdignorecase
import sdinference
import sddeferredbefore
import sddeferredafter
import sdconfig
import sdprint

def run(facets_groups):
    facets_groups=sddeferredbefore.run(facets_groups)
    facets_groups=sdignorecase.run(facets_groups)
    facets_groups=sdinference.run(facets_groups)
    facets_groups=sddeferredafter.run(facets_groups)
    facets_groups=sddecode.run(facets_groups)

    # EXT_PARAM
    #
    # load extensions here
    #
    # TODO

    facets_groups=sdlocal2remote.run(facets_groups)
    facets_groups=sdvalueinputalias.run(facets_groups)
    facets_groups=sdremovefacet.run(facets_groups)
    facets_groups=sddenormodel.run(facets_groups)
    facets_groups=sdvct.run(facets_groups)

    # only vector until this point

    facets_groups=sdvectortoscalar.run(facets_groups)

    # vector and scalar from this point

    if sdconfig.config.getint('behaviour','check_parameter')==1:
        sdcheckparam.run(facets_groups)

    return facets_groups

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
