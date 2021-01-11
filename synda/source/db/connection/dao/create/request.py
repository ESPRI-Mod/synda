# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.models import Connection
from synda.source.db.connection.cursor.models import Cursor


class Request(Connection):
    """
    Request

    """
    def __init__(self, full_filename=""):
        super(Request, self).__init__(full_filename=full_filename)
        self.tbl_names = []
        self.sql = dict()
        self.set_sql()

    def process(self):

        self.execute(
            self.sql["tables"],
        )

        self.execute(
            self.sql["indexes"],
        )

    def tables_already_exist(self):
        res = False

        tbl_names = self.get_tbl_names()
        cursor = Cursor(self.full_filename)

        sql_request = "SELECT * FROM sqlite_master WHERE type='table'"
        cursor.execute(sql_request)
        data = cursor.get_data()
        cursor.close()

        if len(data) == len(tbl_names):
            nb_records = len(tbl_names)
            i = 0
            eod = i >= nb_records
            record = data[i]
            while not eod and record["tbl_name"] in tbl_names:
                i += 1
                eod = i >= nb_records
                if not eod:
                    record = data[i]
            res = i == nb_records
        return res

    def set_sql(self):
        self.sql["tables"] = []
        self.set_sql_tables()
        self.sql["indexes"] = []
        self.set_sql_indexes()

    def get_tbl_names(self):
        return self.tbl_names

    def set_sql_tables(self):
        """
        Notes
            - 'file' table
                - 'file_functional_id' is the functional primary key (same as ESGF 'id', but without data_node,
                   and file extension is cleaned (e.g. '.nc_4' become '.nc'))
                - duration in seconds
                - rate in bytes/seconds
                - size in bytes
                - checksum column contains only *remote* checksum (i.e. if remote checksum doesn't exist,
                  we DON'T store the locally computed checksum in this column (nor anywhere else))
                - 'model' column contains non-normalized model name
                - timestamp column contains is the ESGF timestamp attribute (aka
                  "last update"). Note that this information (file level
                  timestamp) is not used, so it may be removed in future version to
                  gain some space. But maybe it will be usefull to have it so to
                  do some version checking at file level (i.e. have a 'latest' flag
                  in the 'file' table). In this case, the file 'version' attribute
                  will be needed as well (currently this attribute is not stored in
                  Synda).
            - 'dataset' table
                - 'model' column contains non-normalized model name
                - 'path' and 'dataset_functional_id' contain the same value, but with different delimiter
                - timestamp column contains is the ESGF timestamp attribute (aka "last update")
            - 'generic_cache' table
                - 'realm' column is a group of keys/values (e.g. rtt, geo, etc..)
            - 'history' table
                - 'selection_file' column is not used (it was initially added in
                  case 'selection_filename' column would not be sufficient for
                  incremental mode. It may be removed by 2018, once we are sure
                  we don't need it).
            - other tables
                - a dataset is a set of one or more variables
                - 'file_without_dataset' table contains orphan files (dataset doesn't exist for those files)
        """
        self.tbl_names = [
            "file",
            "dataset",
            "export",
            "selection",
            "selection__file",
            "file_without_selection",
            "file_without_dataset",
            "param",
            "version",
            "history",
            "event",
            "generic_cache",
            "failed_url",
        ]
        self.sql["tables"].append(
            "create table if not exists file "
            "(file_id INTEGER PRIMARY KEY, "
            "url TEXT, file_functional_id TEXT, "
            "filename TEXT, "
            "local_path TEXT, "
            "data_node TEXT, "
            "checksum TEXT, "
            "checksum_type TEXT, "
            "duration INT, "
            "size INT, "
            "rate INT, "
            "start_date TEXT, "
            "end_date TEXT, "
            "crea_date TEXT, "
            "status TEXT, "
            "error_msg TEXT, "
            "sdget_status TEXT, "
            "sdget_error_msg TEXT, "
            "priority INT, "
            "tracking_id TEXT, "
            "model TEXT, "
            "project TEXT, "
            "variable TEXT, "
            "last_access_date TEXT, "
            "dataset_id INT, "
            "insertion_group_id INT, "
            "timestamp TEXT)",
        )
        self.sql["tables"].append(
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
            "timestamp TEXT)",
        )

        self.sql["tables"].append(
            "create table if not exists "
            "export (dataset_id INTEGER, "
            "export_date TEXT)",
        )

        self.sql["tables"].append(
            "create table if not exists selection "
            "(selection_id INTEGER PRIMARY KEY, "
            "filename TEXT, "
            "checksum TEXT,status TEXT)",
        )

        self.sql["tables"].append(
            "create table if not exists selection__file "
            "(selection_id INT NOT NULL, "
            "file_id INT NOT NULL)",
        )

        self.sql["tables"].append(
            "create table if not exists file_without_selection (file_id INTEGER)",
        )

        self.sql["tables"].append(
            "create table if not exists file_without_dataset (file_id INTEGER)",
        )

        self.sql["tables"].append(
            "create table if not exists param (name TEXT, value TEXT)",
        )

        self.sql["tables"].append(
            "create table if not exists version (version TEXT)",
        )

        self.sql["tables"].append(
            "create table if not exists history "
            "(history_id INTEGER PRIMARY KEY, "
            "action TEXT, "
            "selection_filename TEXT, "
            "crea_date TEXT, "
            "insertion_group_id INT, "
            "selection_file_checksum TEXT, "
            "selection_file TEXT)",
        )

        self.sql["tables"].append(
            "create table if not exists event "
            "(event_id INTEGER PRIMARY KEY, "
            "name TEXT, status TEXT, "
            "project TEXT, "
            "model TEXT, "
            "dataset_pattern TEXT, "
            "variable TEXT, "
            "filename_pattern TEXT, "
            "crea_date TEXT, "
            "priority INT)",
        )

        self.sql["tables"].append(
            "create table if not exists generic_cache (realm TEXT, name TEXT, value TEXT)",
        )

        self.sql["tables"].append(
            "CREATE TABLE if not exists failed_url ( url_id INTEGER PRIMARY KEY, url TEXT, file_id INTEGER)",
        )

        # self.connection.commit()

    def set_sql_indexes(self):

        self.sql["indexes"].append(
            "create index if not exists idx_file_1 on file (status)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_2 on file (priority)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_3 on file (crea_date)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_file_4 on file (file_functional_id)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_5 on file (dataset_id)",
        )
        # not uniq (when fetching two different versions of the same dataset,
        # many identical file are duplicated, resulting in tracking_id duplicates)
        self.sql["indexes"].append(
            "create index if not exists idx_file_6 on file (tracking_id)",
        )
        # not uniq (when fetching two different versions of the same dataset,
        # many identical file are duplicated, resulting in checksum duplicates)
        self.sql["indexes"].append(
            "create index if not exists idx_file_7 on file (checksum)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_8 on file (insertion_group_id)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_9 on file (project)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_10 on file (model)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_11 on file (filename)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_file_12 on file (local_path)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_dataset_1 on dataset (dataset_functional_id)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_dataset_2 on dataset (status)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_dataset_3 on dataset (path_without_version)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_dataset_4 on dataset (path)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_dataset_5 on dataset (local_path)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_export_1 on export (dataset_id)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_selection_1 on selection (filename)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_selection__file_1 on selection__file (selection_id, file_id)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_without_selection_1 on file_without_selection (file_id)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_without_dataset_1 on file_without_dataset (file_id)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_param_1 on param (name,value)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_event_1 on event (name)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_event_2 on event (status)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_event_3 on event (crea_date)",
        )
        self.sql["indexes"].append(
            "create index if not exists idx_file_13 on file (data_node)",
        )
        self.sql["indexes"].append(
            "create unique index if not exists idx_failed_url_1 on failed_url (url)",
        )


if __name__ == '__main__':
    r = Request()
