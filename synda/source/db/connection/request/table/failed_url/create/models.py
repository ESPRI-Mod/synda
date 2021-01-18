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
        super(Table, self).__init__("table", table_name="failed_url")
        self.set_sql(
            "CREATE TABLE if not exists {} ( url_id INTEGER PRIMARY KEY, url TEXT, file_id INTEGER)".format(
                self.get_table_name(),
            ),
        )


class IndexOnUrl(Request):
    """
    """
    def __init__(self):
        super(IndexOnUrl, self).__init__(
            "index on url",
            table_name="failed_url",
            index_name="idx_failed_url_1",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (url)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
