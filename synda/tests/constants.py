# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda import tests

# RESOURCES ARE REQUIRED FOR BUILDING the contents of the tests/data directory

RESOURCES_DIR = os.path.join(
    os.path.dirname(tests.__file__),
    'resources',
)


def is_test_mode_activated():
    test_mode_activated = False
    if "ST_TESTS_MODE_STATUS" in os.environ:
        if os.environ["ST_TESTS_MODE_STATUS"] == "activated":
            test_mode_activated = True
    return test_mode_activated

# SQLITE DATABASE CONFIG


# 2 minute timeout
DB_CONNECTION_TIMEOUT = 120
