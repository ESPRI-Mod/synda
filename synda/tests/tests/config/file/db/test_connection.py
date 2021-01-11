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

 object : Connection

"""
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.db.connection.models import Connection


@pytest.mark.on_all_envs
def test_connection():

    connection = Connection()
    assert connection.is_valid()
    connection.close()

