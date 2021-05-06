# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class InsertFailedUrl(Request):
    """
    Request

    """
    def __init__(self):
        super(InsertFailedUrl, self).__init__(
            table_name="failed_url",
            identifier="insert_into_failed_url",
        )
        # init

        self.set_sql(
            "INSERT INTO failed_url(url,file_id) VALUES (?, (SELECT file_id FROM file WHERE file_functional_id=?))",
        )
