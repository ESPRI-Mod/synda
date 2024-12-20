# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.constants import RESOURCES_DIR

ENV_NOT_FOUND = "WARNING if you are not building your synda local environment " \
                "(else do not take into account the following message) : " \
                "Your synda local environment has not been found (use init-env sub command to built it)"

IDENTIFIER = "file that contains environment"

FILENAME = "tree.tar.gz"

DEFAULT_FULL_FILENAME = os.path.join(*[RESOURCES_DIR, "environment", FILENAME])

SUB_DIRECTORIES = [
    "bin",
    "conf",
    "data",
    "db",
    "log",
    "recipe",
    "sandbox",
    "selection",
    "tmp",
]
