#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script runs "generic" pipeline's jobs.

Description
    This pipeline is intended to be run just after retrieving files from Search-API,
    before running type specific pipeline (i.e. sdfilepipeline, sddatasetpipeline).

Note
    generic here means type insensitive (i.e. this pipeline is for both file and dataset).
"""

import argparse
import sdpostxpcleanup
import sdpostxptransform

def run(files):

    files=sdpostxpcleanup.run(files)   # exclude malformed files

    """
    sdpostxptransform must be after sdpostxpcleanup as some malformed
    files cannot be proceeded by sdpostxptransform (e.g. for malformed files with
    many variables set, array to scalar cast failed).
    """
    
    files=sdpostxptransform.run(files) # cast

    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
