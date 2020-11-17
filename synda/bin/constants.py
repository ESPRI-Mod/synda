# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.constants import ST_HOME_TESTS
from synda.tests.constants import is_test_mode_activated

ST_HOME = os.environ["ST_HOME"]

SANDBOX_FOLDER = os.path.join(
    ST_HOME,
    "sandbox",
)


def get_home_folder():
    return ST_HOME_TESTS if is_test_mode_activated() else os.environ['ST_HOME']
