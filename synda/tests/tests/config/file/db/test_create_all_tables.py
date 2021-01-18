# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Tests driven by pytest

 object : Table creation & cursor

"""
import os
import pytest
from synda.tests.manager import Manager

manager = Manager()
manager.set_tests_mode()
from synda.source.constants import get_env_folder
from synda.source.db.connection.models import Connection
from synda.source.db.connection.request.tables.dao.create.manager import Manager as CreateManager


@pytest.mark.on_all_envs
def test_create_all_tables():

    full_filename = os.path.join(
        os.path.join(
            get_env_folder(),
            "db",
        ),
        "sdt_empty.db",
    )
    conn = Connection(full_filename=full_filename, timeout=30)

    # tables creation

    tables_manager = CreateManager()
    tables_manager.process_tables(conn)

    # table existence test

    expected_table_names = tables_manager.get_table_names()
    read_tables_manager = conn.get_item("tables crud").get_item("read")
    read_tables_manager.set_db_connection(conn)
    table_names = read_tables_manager.get_table_names()
    assert sorted(table_names) == sorted(expected_table_names)

    index_names = read_tables_manager.get_index_names()
    expected_index_names = tables_manager.get_index_names()
    assert sorted(index_names) == sorted(expected_index_names)

    conn.close()


@pytest.mark.on_all_envs
def test_create_all_tables_error():

    full_filename = os.path.join(
        os.path.join(
            get_env_folder(),
            "db",
        ),
        "sdt_empty.db",
    )
    conn = Connection(full_filename=full_filename, timeout=30)

    # tables creation

    create_manager = CreateManager()
    create_manager.process_tables(conn)

    # table drop

    delete_tables_manager = conn.get_item("tables crud").get_item("delete")
    delete_tables_manager.set_db_connection(conn)
    delete_tables_manager.process_tables(["version"])

    # table existence test

    expected_table_names = create_manager.get_table_names()
    read_tables_manager = conn.get_item("tables crud").get_item("read")
    read_tables_manager.set_db_connection(conn)
    table_names = read_tables_manager.get_table_names()
    assert len(table_names) + 1 == len(expected_table_names)
    assert 'version' not in table_names
