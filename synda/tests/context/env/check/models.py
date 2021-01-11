# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.utils import delete_dirs
from synda.source.process.env.check.models import Config
from synda.source.config.env.check.constants import REQUIRED_FILES
from synda.source.config.env.check.constants import REQUIRED_DIRECTORIES
from synda.source.config.env.check.constants import ERROR_KEY_FILE_MISSING_TEMPLATE
from synda.source.config.env.check.constants import ERROR_KEY_DIRECTORY_MISSING_TEMPLATE
from synda.source.config.env.check.constants import CHECK_COMPLETE

from synda.tests.tests.constants import ST_HOME_TESTS
from synda.tests.context.models import Context as Base


def remove_one_required_file():
    os.remove(
        os.path.join(
            ST_HOME_TESTS,
            REQUIRED_FILES[0],
        )
    )


def remove_one_required_directory():
    delete_dirs(
        os.path.join(
            ST_HOME_TESTS,
            REQUIRED_DIRECTORIES[0],
        )
    )


class Context(Base, Config):

    def __init__(self, capsys=None):
        assert isinstance(capsys, object)
        Base.__init__(self, capsys=capsys)
        Config.__init__(self, ST_HOME_TESTS)

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert CHECK_COMPLETE in captured.out


class OneRequiredFileMissingContext(Base, Config):

    def __init__(self, capsys=None):
        assert isinstance(capsys, object)
        Base.__init__(self, capsys=capsys)
        Config.__init__(self, ST_HOME_TESTS)

        remove_one_required_file()

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert ERROR_KEY_FILE_MISSING_TEMPLATE.format(
            REQUIRED_FILES[0],
        ) in captured.out


class OneRequiredDirectoryMissingContext(Base, Config):

    def __init__(self, capsys=None):
        assert isinstance(capsys, object)
        Base.__init__(self, capsys=capsys)
        Config.__init__(self, ST_HOME_TESTS)

        remove_one_required_directory()

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert ERROR_KEY_DIRECTORY_MISSING_TEMPLATE.format(
            REQUIRED_DIRECTORIES[0],
        ) in captured.out
