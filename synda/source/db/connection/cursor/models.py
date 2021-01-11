# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sqlite3
import itertools

from synda.source.db.connection.models import Connection
from synda.source.db.connection.exceptions import DataIntegrityError, DataUnexpectedError
from synda.source.db.connection.cursor.exceptions import CursorNotAvailable


class Cursor(Connection):

    def __init__(self, full_filename=""):
        super(Cursor, self).__init__(full_filename=full_filename)
        self.db_cursor = None
        self.set_db_cursor()

    def set_db_cursor(self):
        if self.get_database_connection():
            try:
                self.db_cursor = self.get_database_connection().cursor()
            except Exception as error:
                raise CursorNotAvailable(
                    "sqlite",
                    error.__str__(),
                )

    def get_db_cursor(self):
        return self.db_cursor

    def execute(self, sql):
        try:
            self.db_cursor.execute(sql)
        except sqlite3.IntegrityError as error:
            self.close()
            raise DataIntegrityError(
                error.__str__(),
            )
        except Exception as error:
            self.close()
            raise DataUnexpectedError(
                error.__str__(),
            )

        return self.db_cursor

    def close(self):
        self.db_cursor.close()
        super(Cursor, self).close()

    def get_data(self):
        desc = self.db_cursor.description
        column_names = [col[0] for col in desc]
        return [
            dict(itertools.izip_longest(column_names, row)) for row in self.db_cursor.fetchall()
        ]


if __name__ == '__main__':

    cursor = Cursor()
    sql_request = "select version from version"
    cursor.execute(sql_request)
    data = cursor.get_data()
    cursor.close()
    pass
