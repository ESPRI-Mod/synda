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

from synda.source.db.connection.exceptions import DataIntegrityError, DataUnexpectedError
from synda.source.db.connection.cursor.exceptions import CursorNotValid


class Cursor(object):

    def __init__(self, db_cursor, db_identifier=""):
        # init
        self.db_cursor = None
        self.db_identifier = ""

        # settings
        self.set_db_cursor(db_cursor)
        self.db_identifier = db_identifier

    def set_db_cursor(self, db_cursor):
        self.db_cursor = db_cursor

    def get_db_cursor(self):
        return self.db_cursor

    def execute(self, sql, args=None):
        success = False
        if self.db_cursor:
            try:
                if args:
                    self.db_cursor.execute(sql, args)
                else:
                    self.db_cursor.execute(sql)
                success = True

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
        else:
            raise CursorNotValid(
                self.db_identifier,
                "is None",
            )

        return success

    def close(self):
        self.db_cursor.close()

    def get_data(self):
        desc = self.db_cursor.description
        column_names = [col[0] for col in desc]
        return [
            dict(itertools.zip_longest(column_names, row)) for row in self.db_cursor.fetchall()
        ]


if __name__ == '__main__':

    cursor = Cursor()
    sql_request = "select version from version"
    cursor.execute(sql_request)
    data = cursor.get_data()
    cursor.close()
    pass
