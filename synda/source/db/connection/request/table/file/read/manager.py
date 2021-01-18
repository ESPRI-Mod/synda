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
from synda.source.db.connection.request.table.dao.read.manager import Manager as Base

from synda.source.db.connection.request.table.file.read.models import Rows as RowsRequest
from synda.source.db.connection.request.table.file.read.models import DataNodes as DataNodesRequest
from synda.source.db.connection.request.table.file.read.models import SelectAllByFileId as SelectAllByFileIdRequest
from synda.source.db.connection.request.table.file.read.models import \
    DataNodePriorityFilteredOnStatusWaiting as DataNodePriorityFilteredOnStatusWaitingRequest

table_name = RowsRequest().get_table_name()


class Manager(Base):

    def __init__(self):
        Base.__init__(self, table_name=table_name)

        self.add(
            RowsRequest(),
        )
        self.add(
            DataNodesRequest(),
        )
        self.add(
            DataNodePriorityFilteredOnStatusWaitingRequest(),
        )
        self.add(
            SelectAllByFileIdRequest(),
        )

    def get_data_nodes(self):
        request = self.get_item("data_nodes")
        return self.get_request_data(request)

    def get_rows(self):
        request = self.get_item("rows")
        return self.get_request_data(request)

    def get_data_node_priority_filtered_on_status_waiting(self, data_node):
        request = self.get_item("data_node_priority_filtered_on_status_waiting")
        return self.get_request_data(request, (data_node,))

    def get_rows_filtered_on_file_functional_id(self, file_functional_id):
        request = self.get_item("rows_filtered_on_file_functional_id")
        return self.get_request_data(request, (file_functional_id,))
