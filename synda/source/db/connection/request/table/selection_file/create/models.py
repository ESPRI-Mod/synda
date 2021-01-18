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
        - 'selection_file' column is not used (it was initially added in
          case 'selection_filename' column would not be sufficient for
          incremental mode. It may be removed by 2018, once we are sure
          we don't need it).
    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="selection__file")
        self.set_sql(
            "create table if not exists {} "
            "(selection_id INT NOT NULL, "
            "file_id INT NOT NULL)".format(
                self.get_table_name(),
            ),
        )


class IndexOnSelectionIdFileId(Request):
    """
    """
    def __init__(self):
        super(IndexOnSelectionIdFileId, self).__init__(
            "index on selection_id, file_id",
            table_name="selection__file",
            index_name="idx_selection__file_1",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (selection_id, file_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
