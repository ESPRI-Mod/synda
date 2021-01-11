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

from synda.tests.tests.constants import PREFERENCES_USER_FILE_HOME_TESTS
from synda.source.config.file.user.readers import get_parser
from synda.source.config.file.user.preferences.constants import DEFAULT_OPTIONS
from synda.source.config.file.user.preferences.constants import FILENAME as PREFERENCES_FILENAME


fullfilename = os.path.join(
    PREFERENCES_USER_FILE_HOME_TESTS,
    PREFERENCES_FILENAME,
)

parser = get_parser(fullfilename, DEFAULT_OPTIONS)


@pytest.mark.on_all_envs
def test_reader_interface_progress():
    assert parser.get('interface', 'progress') == '0'


@pytest.mark.on_all_envs
def test_reader_download_direct_http_timeout():
    assert parser.get('download', 'direct_http_timeout') == '60'


@pytest.mark.on_all_envs
def test_reader_download_async_http_timeout():
    assert parser.get('download', 'async_http_timeout') == '120'
