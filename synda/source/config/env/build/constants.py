# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.constants import SYNDA_DIR

DIRECTORY = os.path.join(
    SYNDA_DIR,
    'build',
)

TREE_DIRECTORY = os.path.join(
    DIRECTORY,
    "tree",
)
