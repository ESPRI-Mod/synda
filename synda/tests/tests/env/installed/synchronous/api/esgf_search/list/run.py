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

from synda.tests.context.api.esgf_search.list.constants import ENVS
from synda.tests.tests.env.installed.synchronous.api.esgf_search.constants import TESTS_DIR
from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.utils import run_simple_tests


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def tests(coverage_activated=False):

    source = ENVS["installed"]["env"]["full_filename"]
    manager.create_test_environment(source=source)

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("list"),
    )

    run_simple_tests(fullfilenames, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager.delete_test_environment()

    tests(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

