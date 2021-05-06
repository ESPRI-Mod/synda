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
from synda.source.db.connection.exceptions import DataIntegrityError, DataUnexpectedError
from synda.source.db.connection.request.noresultset.manager import Manager as Base
from synda.source.db.connection.request.table.manager import TableName


class Manager(Base, TableName):

    def __init__(self, table_name=""):
        Base.__init__(self, identifier="create")
        TableName.__init__(self, table_name=table_name)

    def get_index_names(self):
        names = []
        for item in self.get_data():
            name = item.get_index_name()
            if name:
                names.append(name)
        return names

    def create(self, connection=None):
        success = False
        if connection:
            self.set_db_connection(connection)
        else:
            connection = self.get_db_connection()
        if connection:
            with connection.get_database_connection():
                for request in self.get_data():
                    success = self.process(request)

        return success
