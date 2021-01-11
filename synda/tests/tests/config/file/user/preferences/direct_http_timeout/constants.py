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

subdirectories = [
    ROOT,
    "file",
    "user",
    "preferences",
    "direct_http_timeout_not_in_preferences",
]

VARIABLE_NOT_IN_PREFERENCES_DIR = os.path.join(*subdirectories)

subdirectories = [
    ROOT,
    "file",
    "user",
    "preferences",
]

VARIABLE_IN_PREFERENCES_DIR = os.path.join(*subdirectories)
