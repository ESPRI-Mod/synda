# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.tests.constants import DATADIR as ROOT
from synda.source.config.file.env.constants import FILENAME as ENV_FILENAME
from synda.tests.process.envs.constants import DATA_DIRECTORY

FUNCTIONAL_DIRECTORY_NAME = "env0"

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

subdirectories = [
    ROOT,
    "envs",
    "env0",
    "get",
    "confirm",
]

SUBCOMMAND_GET_CONFIRM_ANSWER_DIR = os.path.join(*subdirectories)

SUBCOMMAND_GET_CONFIRM_ANSWER_FILE = os.path.join(
    SUBCOMMAND_GET_CONFIRM_ANSWER_DIR,
    "answer.txt",
)