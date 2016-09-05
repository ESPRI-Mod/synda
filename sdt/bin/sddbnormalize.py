#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains database upgrade routines.

Note
    This module is used by sddb, so do not import sddb here.
"""

import sdapp
import sdnormalize
import sdprogress

def normalize_checksum_type(conn):

    dbpagination=DBPagination('bla','foo',sdconst.PROCESSING_CHUNKSIZE,conn)
    dbpagination.reset()

    files=dbpagination.get_files()
    while len(files)>0:
        for t in files:

            checksum_type=sdnormalize.normalize_checksum_type(t.checksum_type)
            update_checksum_type(checksum_type,t.file_id)
            update_db(l__date,t.file_id)

        sddb._conn.commit() # commit block
        conn.commit() # commit block
        sdprogress.SDProgressDot.print_char(".")
        transfers=get_files_pagination()

        files=dbpagination.get_files()

    sdlargequery.get_files_pagination__reset()
