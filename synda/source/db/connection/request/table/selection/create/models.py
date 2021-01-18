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
        super(Table, self).__init__("table", table_name="selection")
        self.set_sql(
            "create table if not exists {} "
            "(selection_id INTEGER PRIMARY KEY, "
            "filename TEXT, "
            "checksum TEXT,status TEXT)".format(
                self.get_table_name(),
            ),
        )


class IndexOnFilename(Request):
    """
    """
    def __init__(self):
        super(IndexOnFilename, self).__init__(
            "index on filename",
            table_name="selection",
            index_name="idx_selection_1",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (filename)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
