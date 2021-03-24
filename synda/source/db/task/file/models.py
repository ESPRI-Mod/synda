# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.models import Connection


def get_data_nodes():
    conn = Connection()
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_data_nodes()
    conn.close()

    return data


def get_rows():
    conn = Connection()
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows()
    conn.close()

    return data


def get_data_node_priority_filtered_on_status_waiting(data_node):
    conn = Connection()
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_data_node_priority_filtered_on_status_waiting(data_node)
    conn.close()

    return data


def get_rows_filtered_on_file_functional_id(file_functional_id):
    conn = Connection()
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_filtered_on_file_functional_id(file_functional_id)
    conn.close()

    return data


if __name__ == '__main__':
    all_data = get_rows()
    data_id = get_rows_filtered_on_file_functional_id(all_data[0]["file_functional_id"])

    data = get_data_nodes()
    priority_data = get_data_node_priority_filtered_on_status_waiting(data[0]["data_node"])
