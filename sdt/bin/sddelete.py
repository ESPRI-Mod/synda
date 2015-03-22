#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synchro-data
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @svn_file       $Id: sddelete.py 12605 2014-03-18 07:31:36Z jerome $
# @version        $Rev: 12611 $
# @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
# @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################
 
"""This module contains delete filter."""

import sys
import os
import json
import argparse
import sdapp
import sddao
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

        sddao.add_history_line(sdconst.ACTION_DELETE,selection_filename)

        sdlog.info("SDDELETE-929","%i files marked for deletion (selection=%s)"%(count,selection_filename))

    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)
