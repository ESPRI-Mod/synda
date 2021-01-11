# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.manager import Manager as Base
from synda.source.identifier import Identifier

from synda.source.constants import get_env_folder
from synda.tests.constants import is_test_mode_activated

from synda.source.process.env.init.models import Config as InitProcess
from synda.source.process.env.init.constants import IDENTIFIER as INIT_PROCESS_IDENTIFIER

from synda.source.process.env.build.models import Process as BuildProcess
from synda.source.process.env.build.constants import IDENTIFIER as BUILD_PROCESS_IDENTIFIER
from synda.source.config.env.build.constants import TREE_DIRECTORY as BUILD_TREE_DIRECTORY
from synda.source.config.file.env.models import Config as EnvFile

from synda.source.process.env.check.models import Config as CheckProcess
from synda.source.process.env.check.constants import IDENTIFIER as CHECK_PROCESS_IDENTIFIER


class Manager(Base, Identifier):

    def __init__(self):
        Base.__init__(self)
        Identifier.__init__(self, "ENVIRONMENT MANAGER")
        self.interactive_mode = not is_test_mode_activated()
        self.root = get_env_folder()

        # add init-env process
        self.add(InitProcess())

        # add build-env process
        self.add(
            BuildProcess(
                build_tree_location=BUILD_TREE_DIRECTORY,
                env_file_name=EnvFile().filename,
                env_file_destination=EnvFile().get(),
            ),
        )

        # add check-env process
        self.add(CheckProcess(self.root))

    def init(self, source="", interactive_mode=False):
        config = self.get_item(INIT_PROCESS_IDENTIFIER)
        config.process(self.root, source=source, interactive_mode=interactive_mode)

    def build(self):
        config = self.get_item(BUILD_PROCESS_IDENTIFIER)
        config.process()

    def check(self, interactive_mode=False):
        config = self.get_item(CHECK_PROCESS_IDENTIFIER)
        return config.process(interactive_mode=interactive_mode)

    def delete(self, target):
        config = self.get_item(BUILD_PROCESS_IDENTIFIER)
        config.delete_tree(target)
