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
        Base.__init__(self, identifier="update")
        TableName.__init__(self, table_name=table_name)

    def get_index_names(self):
        names = []
        for item in self.get_data():
            name = item.get_index_name()
            if name:
                names.append(name)
        return names

    def update(self, request, args=None, connection=None):
        success = False
        if connection:
            self.set_db_connection(connection)
        else:
            connection = self.get_db_connection()
        request.set_cursor(self.get_cursor())

        last_row_id = 0
        msg = ""
        try:
            success = request.execute(args=args)
            if success:
                connection.commit()
                last_row_id = request.get_db_cursor().lastrowid

        except DataIntegrityError as error:
            msg = str(error)
        except DataUnexpectedError as error:
            msg = str(error)

        return success, last_row_id, msg
