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

 Configuration item : downloading file
"""
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.config.file.downloading.models import Config as File


@pytest.mark.on_all_envs
def test_downloading_process_is_active():
    file = File()
    file.set_content(f"{10000}")
    assert file.process_is_active(simulation=True)


@pytest.mark.on_all_envs
def test_downloading_process_is_inactive():
    file = File()
    assert not file.process_is_active()
