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
import sdrmduprep
import sdrmdup
import sdlog

def uniq(metadata):

    if metadata.count() < 1:
        return metadata

    # retrieve global flag
    f=metadata.get_one_file()
    keep_replica=sdpostpipelineutils.get_attached_parameter__global([f],'keep_replica')
    functional_id_keyname=sdpostpipelineutils.get_functional_identifier_name(f)

    if keep_replica=='true':
        # Keep replica.
        # In this case, we remove type-A duplicates, but we keep type-B duplicates (i.e. replicas)

        # uniq key => id (i.e. including datanode)

        sdlog.info("SSHRINKU-001","Remove duplicate..")

        metadata=sdrmdup.run(metadata,functional_id_keyname)
    else:
        # Do not keep replica.
        # In this case, we remove type-A and type-B duplicates by randomly keeping one candidate

        # uniq key => instance_id (i.e. excluding datanode)

        sdlog.info("SSHRINKU-002","Remove duplicate and replicate..")

        metadata=sdrmduprep.run(metadata,functional_id_keyname)

    return metadata
