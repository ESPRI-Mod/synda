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

from synda.source.manager import Manager
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.db.connection.exceptions import DatabaseNotFound, DataIntegrityError, DataUnexpectedError

from synda.source.db.connection.request.tables.dao.manager import Manager as CrudTablesRequests
from synda.source.db.connection.request.table.file.manager import Manager as CrudFileTableRequests
from synda.source.db.connection.request.table.dataset.manager import Manager as CrudDatasetTableRequests
from synda.source.db.connection.request.table.export.manager import Manager as CrudExportTableRequests

from synda.source.db.connection.request.table.failed_url.manager import Manager as CrudFailedUrlTableRequests
from synda.source.db.connection.request.table.file_without_dataset.manager \
    import Manager as CrudFileWithoutDatasetTableRequests

from synda.source.db.connection.request.table.file_without_selection.manager \
    import Manager as CrudFileWithoutSelectionTableRequests

from synda.source.db.connection.request.table.generic_cache.manager import Manager as CrudGenericCacheTableRequests

from synda.source.db.connection.request.table.history.manager import Manager as CrudHistoryTableRequests

from synda.source.db.connection.request.table.param.manager import Manager as CrudParamTableRequests

from synda.source.db.connection.request.table.selection.manager import Manager as CrudSelectionTableRequests

from synda.source.db.connection.request.table.selection_file.manager import Manager as CrudSelectionFileTableRequests

from synda.source.db.connection.request.table.version.manager import Manager as CrudVersionTableRequests

from synda.source.db.connection.request.table.dao.delete.manager import Manager as DeleteTableRequests


from synda.source.config.file.db.models import Config as DBFile
from synda.source.db.connection.cursor.exceptions import CursorNotValid


def get_db_connection():
    connection = Connection()
    return connection.get_database_connection()


class Connection(Manager):

    def __init__(self, full_filename="", timeout=0):
        Manager.__init__(self)
        # init

        self.full_filename = ""
        self.timeout = 0
        self.db_connection = None

        # settings

        self.set_fullfilename(full_filename)

        if not timeout:
            timeout = Preferences().download_direct_db_timeout
        self.timeout = timeout
        self.add_requests()
        self.connect()

    def add_requests(self):
        self.set_data(
            [
                CrudTablesRequests(),
                CrudFileTableRequests(),
                CrudDatasetTableRequests(),
                CrudExportTableRequests(),
                CrudFailedUrlTableRequests(),
                CrudFileWithoutDatasetTableRequests(),
                CrudFileWithoutSelectionTableRequests(),
                CrudGenericCacheTableRequests(),
                CrudHistoryTableRequests(),
                CrudParamTableRequests(),
                CrudSelectionTableRequests(),
                CrudSelectionFileTableRequests(),
                CrudVersionTableRequests(),
                DeleteTableRequests(),
            ]
        )

    def get_fullfilename(self):
        return self.full_filename

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

    def rollback(self):
        self.db_connection.rollback()

    def execute(self, sql_requests):

        if isinstance(sql_requests, str):
            sql_requests = [sql_requests]
        try:
            with self.db_connection:
                for sql_request in sql_requests:
                    self.db_connection.process(sql_request)
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

    def get_cursor(self):
        db_cursor = None
        if self.get_database_connection():
            try:
                db_cursor = self.get_database_connection().cursor()
            except Exception as error:
                raise CursorNotValid(
                    "sqlite",
                    error.__str__(),
                )
        if not db_cursor:
            pass
        return db_cursor


if __name__ == '__main__':

    conn = Connection()
    conn.close()
    pass
