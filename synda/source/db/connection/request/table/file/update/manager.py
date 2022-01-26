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
from synda.source.db.connection.request.table.dao.update.manager import Manager as Base
from synda.source.db.connection.request.table.failed_url.create.models import Table
from synda.source.db.connection.request.table.file.update.models import Status
from synda.source.db.connection.request.table.file.update.models import StatusErrorMsg
from synda.source.db.connection.request.table.file.update.models import StatusErrorMsgPriority
from synda.source.db.connection.request.table.file.update.models import Checksum as ChecksumRequest

table_name = Table().get_table_name()


class Manager(Base):

    def __init__(self):
        Base.__init__(self, table_name=table_name)
        self.set_data(
            [
                Status(),
                StatusErrorMsg(),
                StatusErrorMsgPriority(),
                ChecksumRequest(),

            ]
        )

    def checksum(self, file_id, checksum, connection=None):
        request = self.get_item("update_file_checksum")
        return self.update(request, (checksum, file_id), connection=connection)

    def update_file_status(self, file_id, status, connection=None):
        request = self.get_item("update_file_status")
        return self.update(request, (file_id, status), connection=connection)

    def update_file_status_error_msg(self, file_id, status, error_msg, connection=None):
        request = self.get_item("update_file_status_error_msg")
        return self.update(request, (file_id, status, error_msg), connection=connection)

    def update_file_status_error_msg_priority(self, file_id, status, error_msg, priority, connection=None):
        request = self.get_item("update_file_status_error_msg_priority")
        return self.update(request, (file_id, status, error_msg, priority), connection=connection)
