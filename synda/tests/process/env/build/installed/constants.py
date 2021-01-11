# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.constants import RESOURCES_DIR as ROOT_RESOURCES_DIR
from synda.tests.tests.constants import DATADIR

# ROOT DIRECTORY FOR RESOURCES USED FOR TESTS

ENV_RESOURCES_DIRECTORY = os.path.join(
    ROOT_RESOURCES_DIR,
    "env",
)

INSTALLED_ENV_RESOURCES_DIRECTORY = os.path.join(
    ENV_RESOURCES_DIRECTORY,
    "installed",
)

# ROOT DIRECTORY FOR DATA USED FOR TESTS

ENV_DATA_DIRECTORY = os.path.join(
    DATADIR,
    "env",
)

INSTALLED_ENV_DATA_DIRECTORY = os.path.join(
    ENV_DATA_DIRECTORY,
    "installed",
)
