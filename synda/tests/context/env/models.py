# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from glob import glob
from shutil import copyfile

from synda.source.constants import ST_HOME

from synda.tests.context.models import Context as Base
from synda.source.process.env.manager import Manager


from synda.source.config.file.env.constants import SUB_DIRECTORIES as ENV_SUB_DIRECTORIES
from synda.source.config.file.user.preferences.dao.update.models import update_paths as preferences_update_paths
from synda.source.config.file.user.credentials.constants import FILENAME as CREDENTIALS_FILENAME


class Context(Base, Manager):

    def __init__(self, capsys=None):
        Base.__init__(self, capsys=capsys)
        Manager.__init__(self)

        self.locations = dict()

        self.set_locations()

    def create(self, source="", with_credentials=True):
        self.create_root()
        self.init(source=source, interactive_mode=False)
        if with_credentials:
            self.overwrite_credentials()
        preferences_update_paths()

    def create_root(self):

        if not os.path.isdir(self.root):
            os.mkdir(self.root)
            os.chmod(self.root, 0o755)

    def set_locations(self):
        # create sub directories
        for subdirectory in ENV_SUB_DIRECTORIES:
            self.locations[subdirectory] = os.path.join(
                self.root,
                subdirectory,
            )

    def reset(self):
        subdirectories = ["db", "sandbox", "tmp", "log"]
        for subdirectory in subdirectories:
            files_pattern = os.path.join(
                self.locations[subdirectory],
                "*.*",
            )
            for f in glob(files_pattern):
                os.remove(f)

    def overwrite_credentials(self):

        filename = CREDENTIALS_FILENAME
        directory = "conf"

        conf_location = os.path.join(
            ST_HOME,
            directory,
        )
        src = os.path.join(

            conf_location,
            filename,
        )

        conf_tests_location = os.path.join(
                self.root,
                directory,
            )

        dst = os.path.join(
            conf_tests_location,
            filename,
        )

        copyfile(src, dst)
