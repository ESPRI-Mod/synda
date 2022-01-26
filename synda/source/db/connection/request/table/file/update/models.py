# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class Status(Request):
    """
    Request

    """
    def __init__(self):
        super(Status, self).__init__(
            table_name="file",
            identifier="update_file_status",
        )
        # init

        self.set_sql(
            f"UPDATE {self.get_table_name()} SET status=? WHERE file_id=?",
        )


class StatusErrorMsg(Request):
    """
    Request

    """
    def __init__(self):
        super(StatusErrorMsg, self).__init__(
            table_name="file",
            identifier="update_file_status_error_msg",
        )
        # init

        self.set_sql(
            f"UPDATE {self.get_table_name()} SET status=?,error_msg=? WHERE file_id=?",
        )


class StatusErrorMsgPriority(Request):
    """
    Request

    """
    def __init__(self):
        super(StatusErrorMsgPriority, self).__init__(
            table_name="file",
            identifier="update_file_status_error_msg_priority",
        )
        # init

        self.set_sql(
            f"UPDATE {self.get_table_name()} SET status=?,error_msg=?,priority=? WHERE file_id=?",
        )


class Checksum(Request):
    """
    Request

    """
    def __init__(self):
        super(Checksum, self).__init__(
            table_name="file",
            identifier="update_file_checksum",
        )
        # init

        self.set_sql(
            f"UPDATE {self.get_table_name()} SET checksum=? WHERE file_id=?",
        )
