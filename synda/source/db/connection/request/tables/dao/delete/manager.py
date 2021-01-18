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
from synda.source.db.connection.request.noresultset.manager import Manager as Base
from synda.source.db.connection.request.table.dao.delete.manager import Manager as DeleteTable


class Manager(Base):

    def __init__(self):
        Base.__init__(self, identifier="delete")
        self.add(
            DeleteTable(),
        )

    def process_tables(self, table_names):
        connection = self.get_db_connection()
        request = self.get_item("delete").get_item("drop")
        request.set_cursor(self.get_cursor())
        with connection.get_database_connection():
            for name in table_names:
                success = request.execute((name,))
