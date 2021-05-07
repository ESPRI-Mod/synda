# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.process.env.build.installed.constants import INSTALLED_ENV_RESOURCES_DIRECTORY
from synda.tests.process.env.build.installed.constants import INSTALLED_ENV_DATA_DIRECTORY

FUNCTIONAL_DIRECTORY_NAME = "remove"

RESOURCES_DIRECTORY = os.path.join(
    INSTALLED_ENV_RESOURCES_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)

DB_RESOURCES_DIRECTORY = os.path.join(
    RESOURCES_DIRECTORY,
    "db",
)

DATA_RESOURCES_DIRECTORY = os.path.join(
    RESOURCES_DIRECTORY,
    "data",
)

DATA_DIRECTORY = os.path.join(
    INSTALLED_ENV_DATA_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)
