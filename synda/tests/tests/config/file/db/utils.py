# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import pytest
from synda.tests.manager import Manager

manager = Manager()
manager.set_tests_mode()
from synda.source.db.connection.models import Connection


def create_table(db_file, table_name):

    conn = Connection(full_filename=db_file, timeout=30)

    # 'table_name' table creation

    table_file_manager = conn.get_item(
        "{} table crud".format(
            table_name,
        ),
    ).get_item("create")
    table_file_manager.set_db_connection(conn)
    success = table_file_manager.create()

    # table existence test

    assert success

    read_tables_manager = conn.get_item("tables crud").get_item("read")
    read_tables_manager.set_db_connection(conn)
    table_names = read_tables_manager.get_table_names()
    assert len(table_names) == 1
    assert table_names[0] == table_name

    index_names = read_tables_manager.get_index_names()
    expected_index_names = table_file_manager.get_index_names()
    assert sorted(index_names) == sorted(expected_index_names)

    conn.close()
