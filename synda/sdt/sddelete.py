#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains delete filter."""

import sys
import json
import argparse
from synda.sdt import sdhistorydao
from synda.sdt import sdpostpipelineutils
from synda.sdt import sdsimplefilter
from synda.sdt import sdlog
from synda.sdt import sddeletefile
from synda.sdt import sdpipelineprocessing

from synda.source.db.connection.models import get_db_connection
from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.process.history.constants import STRUCTURE as HISTORY_STRUCT


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

    f = metadata.get_one_file()
    # note that if no files are found at all for this selection (no matter the status), then the filename will be blank
    selection_filename = sdpostpipelineutils.get_attached_parameter__global(
        [f],
        'selection_filename',
    )

    # TODO: merge both to improve perf
    metadata = sdsimplefilter.run(metadata, 'status', TRANSFER["status"]['new'], 'remove')
    metadata = sdsimplefilter.run(metadata, 'status', TRANSFER["status"]['delete'], 'remove')

    count = metadata.count()

    if count > 0:
        po = sdpipelineprocessing.ProcessingObject(delete)
        sdpipelineprocessing.run_pipeline(metadata, po)

        sdhistorydao.add_history_line(
            HISTORY_STRUCT["action"]['delete'],
            selection_filename,
        )

        sdlog.info(
            "SDDELETE-929",
            "%i files marked for deletion (selection=%s)" % (count, selection_filename),
        )

    return count


def delete(files):
    conn = get_db_connection()
    for file in files:
        sddeletefile.deferred_delete(file['file_functional_id'], conn=conn)
    # final commit (we do all update in one transaction).
    conn.commit()
    # nothing to return (end of processing)
    return []


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    _files = json.load(sys.stdin)

    run(_files)
