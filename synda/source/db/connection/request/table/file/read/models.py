# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class AllRows(Request):
    """
    Request

    """
    def __init__(self):
        super(AllRows, self).__init__(table_name="file", identifier="all rows")
        self.set_sql(
            "SELECT * FROM file",
        )


class Row(Request):
    """
    Request

    """
    def __init__(self):
        super(Row, self).__init__(table_name="file", identifier="row")
        self.set_sql(
            "SELECT * FROM file WHERE file_id = ?",
        )

    def get_data(self):
        data = super(Row, self).get_data()
        return data[0]


class Rows(Request):
    """
    Request

    """
    def __init__(self):
        super(Rows, self).__init__(table_name="file", identifier="rows")
        self.set_sql(
            "SELECT * FROM file LIMIT 5",
        )


class DataNodes(Request):
    """
    Request

    """
    def __init__(self):
        super(DataNodes, self).__init__(table_name="file", identifier="data_nodes")
        self.set_sql(
            "SELECT data_node FROM file GROUP BY data_node",
        )

    def get_data(self):
        data = super(DataNodes, self).get_data()
        return [item["data_node"] for item in data]


class DataNodePriorityFilteredOnStatusWaiting(Request):
    """
    Request

    """
    def __init__(self):
        super(DataNodePriorityFilteredOnStatusWaiting, self).__init__(
            table_name="file",
            identifier="data_node_priority_filtered_on_status_waiting",
        )
        # init

        self.set_sql(
            "SELECT MAX(priority) FROM file WHERE status='waiting' AND data_node=?",
        )


class SelectAllByFileId(Request):
    """
    Request

    """
    def __init__(self):
        super(SelectAllByFileId, self).__init__(
            table_name="file",
            identifier="rows_filtered_on_file_functional_id",
        )
        # init

        self.set_sql(
            "select * from file where file_functional_id = ?",
        )
