# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.models import Connection
from synda.source.containers import Container


class Task(Container):

    def __init__(self, db_file=""):
        super(Task, self).__init__(identifier="read file task")
        # init
        self.nb_db_access = 0
        self.connection = None
        self.manager = None
        self.cursor = None

        # settings
        self.connection = Connection(full_filename=db_file)
        self.manager = self.connection.get_item("file table crud").get_item("read")
        self.manager.set_db_connection(self.connection)
        self.cursor = self.manager.get_cursor()

    def report_nb_db_access(self, task_name=""):
        self.nb_db_access += 1
        msg = "nb DB access = {}".format(self.nb_db_access) if not task_name \
            else "nb DB access = {} - DAO : {} - Task name : {}".format(
            self.nb_db_access,
            "file table read",
            task_name
        )
        print(msg)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def get_data_node_priority_filtered_on_status_waiting(self, data_node):
        data = self.manager.get_data_node_priority_filtered_on_status_waiting(data_node, cursor=self.cursor)
        self.report_nb_db_access(task_name="get_data_node_priority_filtered_on_status_waiting")
        return data

    def get_data_nodes(self):
        data = self.manager.get_data_nodes(cursor=self.cursor)
        self.report_nb_db_access(task_name="get_data_nodes")
        return data

    def get_rows_filtered_on_file_functional_id(self, file_functional_id):
        data = self.manager.get_rows_filtered_on_file_functional_id(file_functional_id, cursor=self.cursor)
        self.report_nb_db_access(task_name="get_rows_filtered_on_file_functional_id")
        return data

    def get_number_with_status(self, status):
        data = self.manager.get_rows_number_with_status(status, cursor=self.cursor)
        self.report_nb_db_access(task_name="get_number_with_status")
        return data

    def get_data_nodes_with_status(self, status):
        data = self.manager.get_data_nodes_with_status(status, cursor=self.cursor)
        self.report_nb_db_access(task_name="get_data_nodes_with_status")
        return data

    def get_nb_files_by_data_node(self, data_node):
        data = self.manager.get_nb_rows_by_data_node(data_node, cursor=self.cursor)
        self.report_nb_db_access(task_name="get_nb_files_by_data_node")
        return data

    def get_rows_for_given_status_data_node(self, status, data_node):
        data = self.manager.get_rows_for_given_status_data_node(status, data_node, cursor=self.cursor)
        self.report_nb_db_access(task_name="get_rows_for_given_status_data_node")
        return data


def get_data_nodes(full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_data_nodes()
    conn.close()

    return data


def get_all_rows(full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_all_rows()
    conn.close()

    return data


def get_row(file_id, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_row(file_id)
    conn.close()

    return data


def get_rows(full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows()
    conn.close()

    return data


def get_data_node_priority_filtered_on_status_waiting(data_node, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_data_node_priority_filtered_on_status_waiting(data_node)
    conn.close()

    return data


def get_rows_filtered_on_file_functional_id(file_functional_id, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_filtered_on_file_functional_id(file_functional_id)
    conn.close()

    return data


def get_number_with_status(status, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_number_with_status(status)
    conn.close()

    return data


def get_data_nodes_with_status(status, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_data_nodes_with_status(status)
    conn.close()

    return data


def get_nb_files_by_data_node(data_node, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_nb_rows_by_data_node(data_node)
    conn.close()

    return data


def get_rows_for_given_status_data_node(status, data_node, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_for_given_status_data_node(status, data_node)
    conn.close()

    return data


def get_rows_for_given_status_data_node_limit(status, data_node, limit="", full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_for_given_status_data_node_limit(status, data_node, limit=limit)
    conn.close()

    return data


def get_rows_for_given_status_data_node_priority(status, data_node, priority, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_for_given_status_data_node_priority(status, data_node, priority)
    conn.close()

    return data


def get_rows_for_given_status_data_node_priority_limit(status, data_node, priority, limit, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_for_given_status_data_node_priority_limit(status, data_node, priority, limit)
    conn.close()

    return data


def get_rows_for_given_status_data_node_order_by_priority_checksum(status, data_node, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_for_given_status_data_node_order_by_priority_checksum(status, data_node)
    conn.close()

    return data


def get_rows_for_given_status_data_node_order_by_priority_checksum_limit(status, data_node, limit, full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("file table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_rows_for_given_status_data_node_order_by_priority_checksum_limit(status, data_node, limit)
    conn.close()

    return data


if __name__ == '__main__':
    all_data = get_rows()
    data_id = get_rows_filtered_on_file_functional_id(all_data[0]["file_functional_id"])

    data = get_data_nodes()
    priority_data = get_data_node_priority_filtered_on_status_waiting(data[0]["data_node"])
