# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import sqlite3

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.db.connection.exceptions import DatabaseNotFound, DataIntegrityError, DataUnexpectedError
from synda.source.config.file.db.models import Config as DBFile


class Connection(object):

    def __init__(self, full_filename="", timeout=Preferences().download_direct_db_timeout):

        # init

        self.full_filename = ""
        self.timeout = 0
        self.db_connection = None

        # settings

        self.set_fullfilename(full_filename)
        self.timeout = timeout
        self.connect()

    def set_fullfilename(self, full_filename):

        if full_filename:
            # on demand, the connection is made on a speficic database
            # useful to build the synda environment

            if os.path.isdir(os.path.dirname(full_filename)):
                self.full_filename = full_filename
        else:
            # by default, the connection is made on the operational database
            if DBFile().exists():
                self.full_filename = DBFile().get()

    def close(self):
        self.db_connection.close()
        self.db_connection = None

    def get_database_connection(self):
        return self.db_connection

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    def connect(self):

        try:
            self.db_connection = sqlite3.connect(self.full_filename, self.timeout)
            # this is for "by name" colums indexing
            self.db_connection.row_factory = sqlite3.Row

        except (Exception, sqlite3.DatabaseError) as error:
            raise DatabaseNotFound(
                error.__str__(),
            )

    def is_valid(self):
        return isinstance(self.db_connection, sqlite3.Connection)

    def commit(self):
        self.db_connection.commit()

    def execute(self, sql_requests):

        if isinstance(sql_requests, str):
            sql_requests = [sql_requests]
        try:
            with self.db_connection:
                for sql_request in sql_requests:
                    self.db_connection.execute(sql_request)
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


if __name__ == '__main__':

    conn = Connection()
    conn.close()
    pass
