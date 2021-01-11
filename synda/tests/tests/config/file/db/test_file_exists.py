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

 object : DB file

"""
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.config.file.db.models import Config


@pytest.mark.on_all_envs
def test_file_exists():

    config = Config()
    assert config.exists()
