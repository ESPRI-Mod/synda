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

from synda.source.config.file.db.constants import FILENAME as DB_FILENAME
from synda.source.process.env.build.models import Process as Base
from synda.source.config.file.env.models import Config as EnvFile
from synda.tests.process.env.build.installed.list.constants import DATA_DIRECTORY
from synda.tests.process.env.build.installed.list.constants import DB_RESOURCES_DIRECTORY


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
        self.overwrite_db()

    def overwrite_db(self):
        filename = DB_FILENAME
        src = os.path.join(
            DB_RESOURCES_DIRECTORY,
            filename,
        )

        dst = os.path.join(
            os.path.join(
                self.build_directory,
                "db",
            ),
            filename,
        )
        copyfile(src, dst)

