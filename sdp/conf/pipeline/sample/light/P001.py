#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains P001 pipeline definition."""

import sppipelineutils
import sppostprocessingutils 

def get_pipeline():
    return ppp

# init.

name='P001'

tasks=['remove_duplicate','time_axis_normalization','remove_tmp_files']

ppp=sppostprocessingutils.build_light_pipeline(name,tasks)
