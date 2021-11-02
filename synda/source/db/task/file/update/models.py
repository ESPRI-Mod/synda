# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.models import Connection


def file_status(file_id, status, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("update")
    manager.set_db_connection(conn)
    success = manager.file_status(file_id, status)
    conn.close()

    return success


def file_status_error_msg(file_id, status, error_msg, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("update")
    manager.set_db_connection(conn)
    success = manager.update_file_status_error_msg(file_id, status, error_msg)
    conn.close()

    return success


def file_status_error_msg_priority(file_id, status, error_msg, priority, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("update")
    manager.set_db_connection(conn)
    success = manager.file_status_error_msg_priority(file_id, status, error_msg, priority)
    conn.close()

    return success


if __name__ == '__main__':
    pass