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
        table contains orphan files (dataset doesn't exist for those files)
    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="file_without_dataset")
        self.set_sql(
            "create table if not exists {} (file_id INTEGER)".format(
                self.get_table_name(),
            ),
        )


class IndexOnFileId(Request):
    """
    """
    def __init__(self):
        super(IndexOnFileId, self).__init__(
            "index on file_id",
            table_name="file_without_dataset",
            index_name="idx_file_without_dataset_1",
        )
        self.set_sql(
            "create index if not exists {} on {} (file_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
