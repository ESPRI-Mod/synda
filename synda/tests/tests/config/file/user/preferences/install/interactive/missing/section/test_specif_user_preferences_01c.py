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

 Config         : file/user/preferences
 Specifications : USER-PREFERENCES-01b
"""
import os
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.config.file.user.preferences.models import Config

from synda.tests.tests.config.file.user.preferences.install.interactive.missing.section.constants \
    import PREFERENCES_DIR
from synda.source.config.file.user.preferences.constants import FILENAME as PREFERENCES_FILENAME

full_filename = os.path.join(
    PREFERENCES_DIR,
    PREFERENCES_FILENAME,
)

config = Config(full_filename)


@pytest.mark.on_all_envs
def test_specif_user_preferences_01c():

    assert config.is_install_interactive
