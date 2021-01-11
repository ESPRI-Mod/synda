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

from synda.tests.tests.config.file.user.preferences.async_http_timeout.constants \
    import VARIABLE_IN_PREFERENCES_DIR as PREFERENCES_DIR
from synda.source.config.file.user.preferences.constants import FILENAME as PREFERENCES_FILENAME

full_filename = os.path.join(
    PREFERENCES_DIR,
    PREFERENCES_FILENAME,
)

config = Config(full_filename)


@pytest.mark.on_all_envs
def test_return_preferences_value():
    assert config.download_async_http_timeout == 120
