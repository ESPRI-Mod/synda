#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module reduces the number of files.

Description
    Depending on the context, this filter can do two things: 
    
    Type-A removal: replica instance

        Keep only one instance of each replica. This is needed, because
        in some case (for example with an incorrectly set selection containing
        "variable[*][*]=tas" and "variable[atmos][day]=tas tasmin"), a selection
        can return many copies of the same file). 
    
    Type-B removal: replica

        Keeps only one replica for each file.

Notes
  - This module deals with functional aspects while 'sdreducerow' module deals
    with more technical aspects.
  - This module can be used to process different metadata types (File and Dataset).
"""

import sdpostpipelineutils
import sdnearestpost
import sduniq
import sdconfig

def run(metadata,mode):
    metadata=shrink(metadata)
    return metadata

def shrink(metadata):

    if sdshrinkprepare.is_nearestpost_enabled(metadata):
        # In this case, we remove duplicates by keeping the nearest

        metadata=sdnearestpost.run(metadata)
    else:
        # In this case, we remove duplicates by using a 'uniq' filter

        metadata=remove_duplicate(metadata)

    return metadata

def remove_duplicate():
    keep_replica=sdpostpipelineutils.get_attached_parameter__global(files,'keep_replica')
    if keep_replica=='true':
        # Keep replica.
        # In this case, we remove type-A duplicates, but we keep type-B duplicates (i.e. replicas)

        # uniq key => id (i.e. including datanode)

        files=sduniq.run(files,keep_replica=True)
    else:
        # Do not keep replica.
        # In this case, we remove type-A and type-B duplicates by randomly keeping one candidate

        # uniq key => instance_id (i.e. excluding datanode)

        files=sduniq.run(files)
