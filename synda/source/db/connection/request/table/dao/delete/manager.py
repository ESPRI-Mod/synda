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
from synda.source.db.connection.request.table.manager import TableName
from synda.source.db.connection.request.noresultset.manager import Manager as Base

from synda.source.db.connection.request.table.dao.delete.models import Drop


class Manager(Base, TableName):

    def __init__(self, table_name=""):
        TableName.__init__(self, table_name=table_name)
        Base.__init__(self, identifier="delete")
        self.set_data(
            [
                Drop(),
            ]
        )

    def delete(self, request, table_name, connection=None):
        success = False
        if connection:
            self.set_db_connection(connection)
        else:
            connection = self.get_db_connection()
        if connection:
            with connection.get_database_connection():
                success = self.process(request, (table_name,))

        return success
