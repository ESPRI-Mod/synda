#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains shrink test routines."""

import sdconfig
import sdlmattrfilter
import sdpostpipelineutils
import sdlog

def is_nearestpost_enabled(metadata):
    result=False

    sdlog.debug("SSHRINKT-001","Check if nearestpost is enabled..")

    if sdconfig.nearest_schedule=='post' and nearest_flag_set_on_all_files(metadata):
        result=True
    else:
        result=False

    sdlog.debug("SSHRINKT-002","nearestpost is %s"%result)

    return result

def nearest_flag_set_on_all_files(metadata):
    """This func checks that all files have the 'nearest' flag (as sdnearestpost processing type is 'interfile', we need ALL files to be flagged)."""
    status=True

    # create light list with needed columns only not to overload system memory
    light_metadata=sdlmattrfilter.run(metadata,['attached_parameters']) # we keep 'attached_parameters' because it contains 'nearest' flag we are interested in

    for f in light_metadata.get_files(): # load complete list in memory
        nearest=sdpostpipelineutils.get_attached_parameter(f,'nearest','false')
        if nearest=='false': # one false wins
            status=False
            break

    return status
