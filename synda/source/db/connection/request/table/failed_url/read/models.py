# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class AllRows(Request):
    """
    Request

    """
    def __init__(self):
        super(AllRows, self).__init__(table_name="failed_url", identifier="all rows")
        self.set_sql(
            "SELECT * FROM failed_url",
        )


class RowsWithLimit(Request):
    """
    Request

    """
    def __init__(self):
        super(RowsWithLimit, self).__init__(table_name="failed_url", identifier="rows")
        self.set_sql(
            "SELECT * FROM failed_url LIMIT ?",
        )
