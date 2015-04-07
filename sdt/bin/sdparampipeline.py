#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains 'param' pipeline's tasks.

Note
    This pipeline run *before* the main search-api call.
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
import sdautoextractmodel
import sdinference
import sddeferredbefore
import sddeferredafter
import sdconfig
import sdprint

def run(facets_groups):
    facets_groups=sddeferredbefore.run(facets_groups)
    facets_groups=sdinference.run(facets_groups)
    facets_groups=sddeferredafter.run(facets_groups)
    facets_groups=sddecode.run(facets_groups)
    facets_groups=sdautoextractmodel.run(facets_groups) # we extract the model here so to be able to automatically lock the model
    facets_groups=sdlocal2remote.run(facets_groups)
    facets_groups=sdvalueinputalias.run(facets_groups)
    facets_groups=sdremovefacet.run(facets_groups)
    facets_groups=sddenormodel.run(facets_groups)
    facets_groups=sdvct.run(facets_groups)

    # only vector until this point

    facets_groups=sdvectortoscalar.run(facets_groups)

    # vector and scalar from this point

    # TODO: check if this is needed, as we already do the same in sdinference ...
    if sdconfig.config.getint('behaviour','check_parameter')==1:
        sdcheckparam.run(facets_groups)

    return facets_groups

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
