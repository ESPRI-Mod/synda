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

from synda.tests.tests.utils import run_simple_tests

from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.env.default.synchronous.constants import TESTS_DIR


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def main(coverage_activated=False):

    manager.delete_test_environment()

    manager.create_test_environment()

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("check_env"),
    )

    run_simple_tests(fullfilenames, coverage_activated=coverage_activated)

    # Synchronous MODE, subcommand install (except the part of the process handled by the daemon)

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("install"),
    )

    run_simple_tests(fullfilenames, coverage_activated=coverage_activated)

    # Synchronous MODE, subcommand autoremove

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("autoremove"),
    )

    run_simple_tests(fullfilenames, coverage_activated=coverage_activated)

    # Synchronous MODE, subcommand get

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("get"),
    )

    run_simple_tests(fullfilenames, coverage_activated=coverage_activated)

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("api"),
    )

    run_simple_tests(fullfilenames, coverage_activated=coverage_activated)

    manager.delete_test_environment()


if __name__ == '__main__':
    main()

