# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

import synda
from synda.tests.tests.constants import ST_HOME_TESTS
from synda.tests.constants import is_test_mode_activated

SYNDA_DIR = os.path.dirname(synda.__file__)

RESOURCES_DIR = os.path.join(
    SYNDA_DIR,
    'resources',
)

ST_HOME = os.environ["ST_HOME"]


def get_env_folder():
    return ST_HOME_TESTS if is_test_mode_activated() else os.environ['ST_HOME']


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
