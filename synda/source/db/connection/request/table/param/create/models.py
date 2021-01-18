# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class Table(Request):
    """

    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="param")
        self.set_sql(
            "create table if not exists {} (name TEXT, value TEXT)".format(
                self.get_table_name(),
            ),
        )


class IndexOnNameValue(Request):
    """
    """
    def __init__(self):
        super(IndexOnNameValue, self).__init__(
            "index on name, value",
            table_name="param",
            index_name="idx_param_1",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (name,value)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
