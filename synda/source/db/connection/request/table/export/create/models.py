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
        - a dataset is a set of one or more variables
    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="export")
        self.set_sql(
            "create table if not exists "
            "{} (dataset_id INTEGER, "
            "export_date TEXT)".format(
                self.get_table_name(),
            ),
        )


class IndexOnDatasetId(Request):
    """
    """
    def __init__(self):
        super(IndexOnDatasetId, self).__init__(
            "index on dataset_id",
            table_name="export",
            index_name="idx_export_1",
        )
        self.set_sql(
            "create index if not exists {} on {} (dataset_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
