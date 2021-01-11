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

 Sub-command : GET
 Optional argument : selection_file
 Operating context : file doesn't exist
"""
import os
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.config.file.user.preferences.models import Config

from synda.tests.tests.constants import PREFERENCES_USER_FILE_HOME_TESTS

full_filename = os.path.join(
    PREFERENCES_USER_FILE_HOME_TESTS,
    "sdt.conf",
)

config = Config(full_filename)


@pytest.mark.on_all_envs
def test_model_interface_progress():
    assert not config.is_interface_progress


@pytest.mark.on_all_envs
def test_model_core_metadata_server_type():
    assert config.core_metadata_server_type == "esgf_search_api"


@pytest.mark.on_all_envs
def test_model_interface_progress():
    assert not config.is_interface_progress


@pytest.mark.on_all_envs
def test_model_download_direct_http_timeout():
    assert config.download_direct_http_timeout == 60


@pytest.mark.on_all_envs
def test_model_download_async_http_timeout():
    assert config.download_async_http_timeout == 120
