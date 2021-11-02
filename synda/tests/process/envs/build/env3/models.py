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
from synda.tests.process.envs.build.env3.constants import DATA_DIRECTORY
from synda.tests.process.envs.build.env3.constants import SELECTION_RESOURCES_DIRECTORY
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

    def customize(self):
        self.add_selection_file()

    def add_selection_file(self):
        filenames = ENV["files_selection"]
        for filename in filenames:
            src = os.path.join(
                SELECTION_RESOURCES_DIRECTORY,
                filename,
            )

            dst = os.path.join(
                os.path.join(
                    self.build_directory,
                    "selection",
                ),
                filename,
            )
            copyfile(src, dst)

