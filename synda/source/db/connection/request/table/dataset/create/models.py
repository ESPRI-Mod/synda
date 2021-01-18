# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class Table(Request):
    """
        - 'model' column contains non-normalized model name
        - 'path' and 'dataset_functional_id' contain the same value, but with different delimiter
        - timestamp column contains is the ESGF timestamp attribute (aka "last update")

    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="dataset")
        self.set_sql(
            "create table if not exists dataset "
            "(dataset_id INTEGER PRIMARY KEY, "
            "dataset_functional_id TEXT, "
            "status TEXT, "
            "crea_date TEXT, "
            "path TEXT, "
            "path_without_version TEXT, "
            "version TEXT, "
            "local_path TEXT, "
            "last_mod_date TEXT, "
            "latest INT, "
            "latest_date TEXT, "
            "last_done_transfer_date TEXT, "
            "model TEXT, "
            "project TEXT, "
            "template TEXT, "
            "timestamp TEXT)".format(
                self.get_table_name(),
            ),
        )


class IndexOnDatasetFunctionalId(Request):
    """
    """
    def __init__(self):
        super(IndexOnDatasetFunctionalId, self).__init__(
            "index on dataset_functional_id",
            table_name="dataset",
            index_name="idx_dataset_1",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (dataset_functional_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexStatus(Request):
    """
    """

    def __init__(self):
        super(IndexStatus, self).__init__(
            "index on status",
            table_name="dataset",
            index_name="idx_dataset_2",
        )
        self.set_sql(
            "create index if not exists {} on {} (status)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexPathWithoutVersion(Request):
    """
    """

    def __init__(self):
        super(IndexPathWithoutVersion, self).__init__(
            "index on path_without_version",
            table_name="dataset",
            index_name="idx_dataset_3",
        )
        self.set_sql(
            "create index if not exists {} on {} (path_without_version)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexPath(Request):
    """
    """

    def __init__(self):
        super(IndexPath, self).__init__(
            "index on path",
            table_name="dataset",
            index_name="idx_dataset_4",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (path)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexLocalPath(Request):
    """
    """

    def __init__(self):
        super(IndexLocalPath, self).__init__(
            "index on local_path",
            table_name="dataset",
            index_name="idx_dataset_5",
        )
        self.set_sql(
            "create index if not exists {} on {} (local_path)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
