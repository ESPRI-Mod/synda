# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.process.envs.constants import RESOURCES_DIRECTORY
from synda.tests.process.envs.constants import DATA_DIRECTORY

FUNCTIONAL_DIRECTORY_NAME = "env1"

RESOURCES_DIRECTORY = os.path.join(
    RESOURCES_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)

DB_RESOURCES_DIRECTORY = os.path.join(
    RESOURCES_DIRECTORY,
    "db",
)

PREFERENCES_FILE_RESOURCES_DIRECTORY = os.path.join(
    RESOURCES_DIRECTORY,
    "conf",
)

DATA_DIRECTORY = os.path.join(
    DATA_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)
