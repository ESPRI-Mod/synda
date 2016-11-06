#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""Pipeline dependency loader.

Note
    'sppipelinedep' stands for 'Synda Post-processing PIPELINE DEPendency'
"""

import os
import sys
import imp
import spconfig
from spexception import SPException

sys.path.insert(0, spconfig.pipeline_folder) # this is because of sdpipelineutils.py. TODO: try to find a better way to prevent doing that

def get_module():
    name='spbindings'

    dep_file='%s/%s.py'%(spconfig.pipeline_folder,name)
        
    if not os.path.exists(dep_file):
        raise SPException("SPPIPDEP-001","Pipeline dependency file not found (%s)"%dep_file)

    pipeline_dependency_module=imp.load_source(name, dep_file)

    return pipeline_dependency_module

# init.
