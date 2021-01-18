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
from synda.source.db.connection.cursor.models import Cursor
from synda.tests.tests.config.file.db.utils import create_table


@pytest.mark.on_all_envs
def test_cursor():

    db_file = os.path.join(
        os.path.join(
            get_env_folder(),
            "db",
        ),
        "sdt_empty.db",
    )

    table_name = 'file'
    create_table(db_file, table_name)

    conn = Connection(full_filename=db_file, timeout=30)

    cursor = Cursor(conn.get_cursor())

    sql_request = "SELECT * FROM sqlite_master WHERE type='table'"
    cursor.execute(sql_request)
    data = cursor.get_data()
    cursor.close()

    assert data[0]['name'] == table_name
