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

 object : Table "file" - results comparison between sd... requests and poo requests

"""
import pytest
from synda.tests.manager import Manager

manager = Manager()
manager.set_tests_mode()

from synda.tests.context.envs.env1.subcommand.api.esgf_search.list.constants import ENVS

from synda.source.db.task.file.read.models import get_data_nodes
from synda.source.db.task.file.read.models import get_data_node_priority_filtered_on_status_waiting


@pytest.mark.on_all_envs
def test_compare_data_nodes():
    source = ENVS["installed"]["env1"]["full_filename"]
    manager.create_test_environment(source=source)

    # POO request
    data_node = get_data_nodes()[0]

    # from 'sd...' packages request
    from synda.sdt import sddb
    q = "SELECT data_node FROM file GROUP BY data_node"
    connection = sddb.conn
    c = connection.cursor()
    c.execute(q)
    data_nodes_old = c.fetchone()[0]

    assert data_node == data_nodes_old


@pytest.mark.on_all_envs
def test_compare_data_node_priority_filtered_on_status_waiting():
    source = ENVS["installed"]["env1"]["full_filename"]
    manager.create_test_environment(source=source)

    # POO request
    data_nodes = get_data_nodes()
    data_node = data_nodes[0]
    val = get_data_node_priority_filtered_on_status_waiting(data_node)

    # from 'sd...' packages request
    from synda.sdt import sddb
    q = "SELECT MAX(priority) FROM file WHERE status='waiting' AND data_node='%s'" % data_node
    connection = sddb.conn
    c = connection.cursor()
    c.execute(q)
    val_old = c.fetchone()
    assert val[0]['MAX(priority)'] == val_old[0]
    pass
