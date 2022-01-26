# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
import os
from shutil import copyfile

from synda.source.process.env.build.models import Process as Base
from synda.source.config.file.env.models import Config as EnvFile
from synda.tests.process.envs.build.no_credentials.constants import DATA_DIRECTORY
from synda.tests.context.envs.env3.constants import ENV

BUILD_LOCATION = os.path.join(
    DATA_DIRECTORY,
    "tree",
)


class Process(Base):

    def __init__(
            self,
    ):
        Base.__init__(
            self,
            build_tree_location=BUILD_LOCATION,
            env_file_name=EnvFile().filename,
            env_file_destination=DATA_DIRECTORY,
        )
