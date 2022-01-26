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
        super(AllRows, self).__init__(table_name="dataset", identifier="all rows")
        self.set_sql(
            "SELECT * FROM dataset",
        )


class Row(Request):
    """
    Request

    """
    def __init__(self):
        super(Row, self).__init__(table_name="file", identifier="row")
        self.set_sql(
            "SELECT * FROM file WHERE file_id = ?",
        )

    def get_data(self):
        data = super(Row, self).get_data()
        return data[0]


class Rows(Request):
    """
    Request

    """
    def __init__(self):
        super(Rows, self).__init__(table_name="file", identifier="rows")
        self.set_sql(
            "SELECT * FROM file LIMIT 5",
        )
