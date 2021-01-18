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

from synda.source.db.connection.request.table.file.create.manager import Manager as FileTable
from synda.source.db.connection.request.table.dataset.create.manager import Manager as DatasetTable
from synda.source.db.connection.request.table.export.create.manager import Manager as ExportTable
from synda.source.db.connection.request.table.failed_url.create.manager import Manager as FailedUrlTable

from synda.source.db.connection.request.table.file_without_dataset.create.manager \
    import Manager as FileWithoutDatasetTable

from synda.source.db.connection.request.table.file_without_selection.create.manager \
    import Manager as FileWithoutSelectionTable

from synda.source.db.connection.request.table.generic_cache.create.manager import Manager as GenericCacheTable
from synda.source.db.connection.request.table.history.create.manager import Manager as HistoryTable
from synda.source.db.connection.request.table.param.create.manager import Manager as ParamTable
from synda.source.db.connection.request.table.selection.create.manager import Manager as SelectionTable
from synda.source.db.connection.request.table.selection_file.create.manager import Manager as SelectionFileTable
from synda.source.db.connection.request.table.version.create.manager import Manager as VersionTable


class Manager(Base):

    def __init__(self, identifier="create"):
        Base.__init__(self, identifier=identifier)
        self.set_data(
            [
                DatasetTable(),
                FileTable(),
                ExportTable(),
                FailedUrlTable(),
                FileWithoutDatasetTable(),
                FileWithoutSelectionTable(),
                GenericCacheTable(),
                HistoryTable(),
                ParamTable(),
                SelectionTable(),
                SelectionFileTable(),
                VersionTable(),
            ]
        )

    def get_table_names(self):
        names = []
        for item in self.get_data():
            names.append(
                item.get_table_name(),
            )
        return names

    def get_index_names(self):
        names = []
        for item in self.get_data():
            names.extend(
                item.get_index_names(),
            )
        return names

    def process_tables(self, connection):
        with connection.get_database_connection():
            for manager in self.get_data():
                success = manager.create(connection)
