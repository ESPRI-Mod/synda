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
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.db.connection.models import Connection
from synda.source.db.connection.cursor.models import Cursor
from synda.source.db.connection.dao.create.request import Request


@pytest.mark.on_all_envs
def test_create_all_tables():

    # tables creation

    request = Request()
    request.process()
    tbl_names = request.get_tbl_names()
    # creation control

    cursor = Cursor()

    sql_request = "SELECT * FROM sqlite_master WHERE type='table'"
    cursor.execute(sql_request)
    data = cursor.get_data()
    cursor.close()

    assert len(data) == len(tbl_names)
    assert request.tables_already_exist()


@pytest.mark.on_all_envs
def test_create_all_tables_error():

    # tables creation

    request = Request()
    request.process()
    tbl_names = request.get_tbl_names()

    # table drop

    connection = Connection()
    sql_drop_request = "DROP TABLE version"
    connection.execute(sql_drop_request)
    connection.close()

    # creation control

    cursor = Cursor()

    sql_request = "SELECT * FROM sqlite_master WHERE type='table'"
    cursor.execute(sql_request)
    data = cursor.get_data()
    cursor.close()

    assert len(data) == len(tbl_names) - 1
    assert not request.tables_already_exist()
