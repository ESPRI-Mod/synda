# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.manager import Manager
manager = Manager()
manager.set_tests_mode()

from synda.tests.context.envs.no_credentials.constants import ENV
from synda.tests.tests.envs.no_credentials.subcommand.constants import TESTS_DIR
from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.utils import run_test_under_subprocess


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def tests(coverage_activated=False):

    source = ENV["full_filename"]
    manager.create_test_environment(source=source)

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("get"),
    )

    for fullfilename in fullfilenames:
        run_test_under_subprocess(fullfilename, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager.delete_test_environment()

    tests(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()
