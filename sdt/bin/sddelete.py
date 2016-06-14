#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains delete filter."""

import sys
import os
import json
import argparse
import sdapp
import sdhistorydao
import sdpostpipelineutils
import sdsimplefilter
import sdconst
import sdlog
import sddeletefile

def run(files):
    """
    Set files status to "delete"

    Note
        - the func only change the status (i.e. data and metadata will be removed later by the daemon)
    """
    selection_filename=sdpostpipelineutils.get_attached_parameter__global(files,'selection_filename')

    files=sdsimplefilter.run(files,'status',sdconst.TRANSFER_STATUS_NEW,'remove')
    files=sdsimplefilter.run(files,'status',sdconst.TRANSFER_STATUS_DELETE,'remove')

    count=len(files)

    if count>0:
        for file in files:
            sddeletefile.deferred_delete(file['file_functional_id'])

        sdhistorydao.add_history_line(sdconst.ACTION_DELETE,selection_filename)

        sdlog.info("SDDELETE-929","%i files marked for deletion (selection=%s)"%(count,selection_filename))

    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)
