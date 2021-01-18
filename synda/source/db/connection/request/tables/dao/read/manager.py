# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
from synda.source.db.connection.request.table.dao.read.manager import Manager as Base

from synda.source.db.connection.request.tables.dao.read.models import TableNames as TableNamesRequest
from synda.source.db.connection.request.tables.dao.read.models import IndexNames as IndexNamesRequest


class Manager(Base):

    def __init__(self):
        Base.__init__(self, "read")

        self.set_data(
            [
                TableNamesRequest(),
                IndexNamesRequest(),
            ]
        )

    def get_table_names(self):
        request = self.get_item("table names")
        data = self.get_request_data(request)
        table_names = []
        for row in data:
            table_names.append(
                row['tbl_name']
            )
        return table_names

    def get_index_names(self):
        request = self.get_item("index names")
        data = self.get_request_data(request)
        index_names = []
        for row in data:
            index_names.append(
                row['name']
            )
        return index_names
