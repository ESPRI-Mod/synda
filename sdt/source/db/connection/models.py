# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sqlite3

from sdt.tests.constants import DB_CONNECTION_TIMEOUT
from sdt.source.db.connection.exceptions import DatabaseNotFound, DataIntegrityError, DataUnexpectedError
from sdt.source.db.cursor.models import Cursor
from sdt.source.db.cursor.exceptions import CursorNotAvailable


class Connection(object):

    def __init__(self, full_filename):

        self.full_filename = ""
        self.db_connection = None
        self.cursor = None

        self.full_filename = full_filename

    def set_cursor(self):
        if self.db_connection:
            try:
                self.cursor = Cursor(
                    self.db_connection.cursor()
                )

                pass
            except Exception as error:
                raise CursorNotAvailable(
                    "sqlite",
                    error.__str__(),
                )

    def get_cursor(self):
        return self.cursor

    def get_database_cursor(self):
        if not self.db_connection:
            self.connect()
        if not self.cursor:
            self.set_cursor()
        return self.cursor.get_database_cursor()

    def close(self):
        self.get_database_cursor().close()
        self.db_connection.close()

        self.db_connection = None
        self.cursor = None

    def get_database_connection(self):
        return self.db_connection

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    def connect(self):

        try:
            self.db_connection = sqlite3.connect(self.full_filename, DB_CONNECTION_TIMEOUT)

        except (Exception, sqlite3.DatabaseError) as error:
            raise DatabaseNotFound(
                error.__str__(),
            )

    def execute(self, sql_request):
        cursor = self.get_database_cursor()
        try:
            cursor.execute(sql_request)
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

        return cursor


if __name__ == '__main__':
    import os
    # from sdt.tests.constants import DB_HOME_TESTS
    # full_filename = os.path.join(
    #     DB_HOME_TESTS,
    #     "sdt.db",
    # )

    from sdt.bin.constants import ST_HOME

    full_filename = os.path.join(
        os.path.join(
            ST_HOME,
            "db",
        ),
        "sdt.db",
    )
    conn = Connection(full_filename)
    sql_request = "SELECT * FROM file;"
    # sql_request = "SELECT * FROM selection__file;"
    # sql_request = "SELECT * FROM sqlite_master WHERE type='table'"
    conn.execute(sql_request)
    data = conn.get_cursor().get_data()
    conn.close()
    pass
