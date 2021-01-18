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
        super(Table, self).__init__("table", table_name="history")
        self.set_sql(
            "create table if not exists {} "
            "(history_id INTEGER PRIMARY KEY, "
            "action TEXT, "
            "selection_filename TEXT, "
            "crea_date TEXT, "
            "insertion_group_id INT, "
            "selection_file_checksum TEXT, "
            "selection_file TEXT)".format(
                self.get_table_name(),
            ),
        )
