#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains file normalization filter.

Note
    'sdnormalizefattr' means 'SynDa NORMALIZE File ATTRibute'
"""

import sdnormalize

def run(files):
    for f in files:
        if 'checksum_type' in f:
            f['checksum_type']=sdnormalize.normalize_checksum_type(f['checksum_type'])
    return files
