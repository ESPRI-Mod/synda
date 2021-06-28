# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.config.path.tree.default.models import Config as TreePath
from synda.source.constants import RESOURCES_DIR

IDENTIFIER = "wget exit status"

DIRECTORY = "wget"
FILENAME = "exit_status.txt"

DELIMITER = ";"

DEFAULT_FULL_FILENAME = os.path.join(*[RESOURCES_DIR, DIRECTORY, FILENAME])
