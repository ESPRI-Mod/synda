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
import sddb
import sdpipelineprocessing

def run(metadata):
    """
    Set files status to "delete"

    Returns:
        Number of deleted items.

    Note
        - the func only change the status (i.e. data and metadata will be removed later by the daemon)
    """

    if metadata.count() < 1:
        return 0

    f=metadata.get_one_file()
    selection_filename=sdpostpipelineutils.get_attached_parameter__global([f],'selection_filename') # note that if no files are found at all for this selection (no matter the status), then the filename will be blank

    # TODO: merge both to improve perf
    metadata=sdsimplefilter.run(metadata,'status',sdconst.TRANSFER_STATUS_NEW,'remove')
    metadata=sdsimplefilter.run(metadata,'status',sdconst.TRANSFER_STATUS_DELETE,'remove')

    count=metadata.count()

    if count>0:
        po=sdpipelineprocessing.ProcessingObject(delete)
        metadata=sdpipelineprocessing.run_pipeline(metadata,po)
        sddb.conn.commit() # final commit (we do all update in one transaction).

        sdhistorydao.add_history_line(sdconst.ACTION_DELETE,selection_filename)

        sdlog.info("SDDELETE-929","%i files marked for deletion (selection=%s)"%(count,selection_filename))

    return count

def delete(files):
    for file in files:
        sddeletefile.deferred_delete(file['file_functional_id'])
    return [] # nothing to return (end of processing)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)
