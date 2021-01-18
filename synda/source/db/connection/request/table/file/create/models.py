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

    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="file")
        self.set_sql(
            "create table if not exists {} "
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
            "timestamp TEXT)".format(
                self.get_table_name(),
            ),
        )


class IndexOnStatus(Request):
    """
    """
    def __init__(self):
        super(IndexOnStatus, self).__init__(
            "index on priority",
            table_name="file",
            index_name="idx_file_1",
        )
        self.set_sql(
            "create index if not exists {} on {} (status)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnPriority(Request):
    """
    """
    def __init__(self):
        super(IndexOnPriority, self).__init__(
            "index on priority",
            table_name="file",
            index_name="idx_file_2",
        )
        self.set_sql(
            "create index if not exists {} on {} (priority)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnCreaDate(Request):
    """
    """
    def __init__(self):
        super(IndexOnCreaDate, self).__init__(
            "index on crea_date",
            table_name="file",
            index_name="idx_file_3",

        )
        self.set_sql(
            "create index if not exists {} on {} (crea_date)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnFileFunctionalId(Request):
    """
    """

    def __init__(self):
        super(IndexOnFileFunctionalId, self).__init__(
            "index on file_functional_id",
            table_name="file",
            index_name="idx_file_4",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (file_functional_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnDatasetId(Request):
    """
    """

    def __init__(self):
        super(IndexOnDatasetId, self).__init__(
            "index on dataset_id",
            table_name="file",
            index_name="idx_file_5",
        )
        self.set_sql(
            "create index if not exists {} on {} (dataset_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnTrackingId(Request):
    """
        not uniq (when fetching two different versions of the same dataset,
        many identical file are duplicated, resulting in tracking_id duplicates)
    """

    def __init__(self):
        super(IndexOnTrackingId, self).__init__(
            "index on tracking_id",
            table_name="file",
            index_name="idx_file_6",
        )
        self.set_sql(
            "create index if not exists {} on {} (tracking_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnChecksum(Request):
    """
        not uniq (when fetching two different versions of the same dataset,
        many identical file are duplicated, resulting in checksum duplicates)
    """

    def __init__(self):
        super(IndexOnChecksum, self).__init__(
            "index on checksum",
            table_name="file",
            index_name="idx_file_7",
        )
        self.set_sql(
            "create index if not exists {} on {} (checksum)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnInsertionGroupId(Request):
    """
    """

    def __init__(self):
        super(IndexOnInsertionGroupId, self).__init__(
            "index on insertion_group_id",
            table_name="file",
            index_name="idx_file_8",
        )
        self.set_sql(
            "create index if not exists {} on {} (insertion_group_id)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnProject(Request):
    """
    """

    def __init__(self):
        super(IndexOnProject, self).__init__(
            "index on project",
            table_name="file",
            index_name="idx_file_9",
        )
        self.set_sql(
            "create index if not exists {} on {} (project)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnModel(Request):
    """
    """

    def __init__(self):
        super(IndexOnModel, self).__init__(
            "index on model",
            table_name="file",
            index_name="idx_file_10",
        )
        self.set_sql(
            "create index if not exists {} on {} (model)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnFilename(Request):
    """
    """

    def __init__(self):
        super(IndexOnFilename, self).__init__(
            "index on filename",
            table_name="file",
            index_name="idx_file_11",
        )
        self.set_sql(
            "create index if not exists {} on {} (filename)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )


class IndexOnLocalPath(Request):
    """
    """

    def __init__(self):
        super(IndexOnLocalPath, self).__init__(
            "index on local_path",
            table_name="file",
            index_name="idx_file_12",
        )
        self.set_sql(
            "create unique index if not exists {} on {} (local_path)".format(
                self.get_index_name(),
                self.get_table_name(),
            ),
        )
