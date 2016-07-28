#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains shrink preprocessing routines."""

import sdpostpipelineutils
import sduniq

def uniq(metadata):

    # retrieve global flag
    f=metadata.get_one_file()
    keep_replica=sdpostpipelineutils.get_attached_parameter__global([f],'keep_replica')
    functional_id_keyname=sdpostpipelineutils.get_functional_identifier_name(f)

    if keep_replica=='true':
        # Keep replica.
        # In this case, we remove type-A duplicates, but we keep type-B duplicates (i.e. replicas)

        # uniq key => id (i.e. including datanode)

        metadata=sduniq.run(metadata,functional_id_keyname,keep_replica=True)
    else:
        # Do not keep replica.
        # In this case, we remove type-A and type-B duplicates by randomly keeping one candidate

        # uniq key => instance_id (i.e. excluding datanode)

        metadata=sduniq.run(metadata,functional_id_keyname,keep_replica=False)

    return metadata
