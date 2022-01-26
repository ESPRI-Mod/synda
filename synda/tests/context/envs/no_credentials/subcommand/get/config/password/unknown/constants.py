# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.config.file.env.constants import FILENAME as ENV_FILENAME
from synda.tests.process.envs.constants import DATA_DIRECTORY

subdirectories = [
    "no_credentials",
    "config",
    "password",
    "unknown",
]

FUNCTIONAL_DIRECTORY_NAME = os.path.join(*subdirectories)

DATA_DIRECTORY = os.path.join(
    DATA_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)


ENV = dict(
    full_filename=os.path.join(
        DATA_DIRECTORY,
        ENV_FILENAME,
    ),
)
