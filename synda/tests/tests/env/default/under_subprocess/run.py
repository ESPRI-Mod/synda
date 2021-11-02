# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.tests.utils import run_test_under_subprocess
from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.env.default.under_subprocess.constants import TESTS_DIR
from synda.tests.manager import Manager


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def test_install_filename(manager, coverage_activated=False):

    manager.create_test_environment()

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("install"),
    )

    for fullfilename in fullfilenames:
        run_test_under_subprocess(fullfilename, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def test_getinfo_filename(manager, coverage_activated=False):

    manager.create_test_environment()

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("getinfo"),
    )

    for fullfilename in fullfilenames:
        run_test_under_subprocess(fullfilename, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def test_get_filename(manager, coverage_activated=False):

    manager.create_test_environment()

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("get"),
    )

    for fullfilename in fullfilenames:
        run_test_under_subprocess(fullfilename, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager = Manager()
    manager.set_tests_mode()
    manager.delete_test_environment()

    test_install_filename(manager, coverage_activated=coverage_activated)
    test_getinfo_filename(manager, coverage_activated=coverage_activated)
    test_get_filename(manager, coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

