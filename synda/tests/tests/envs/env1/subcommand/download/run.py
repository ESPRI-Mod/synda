# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
MAIN run for TEST SUITE
it allows to control the tests sequences from the most required to the most advanced ones
"""
import os

from synda.tests.manager import Manager
manager = Manager()
manager.set_tests_mode()

from synda.tests.context.envs.env1.constants import ENV
from synda.tests.tests.envs.env1.constants import TESTS_DIR
from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.utils import run_test_under_subprocess
from synda.tests.tests.envs.env1.subcommand.download.start.run import main as run_env1_download_start
from synda.tests.tests.envs.env1.subcommand.download.stop.run import main as run_env1_download_stop

def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def tests(coverage_activated=False):

    source = ENV["full_filename"]
    manager.create_test_environment(source=source)

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("download"),
    )

    filtererd_fullfilenames = []
    for fullfilename in fullfilenames:
        if not "start" in fullfilename and not "stop" in fullfilename:
            filtererd_fullfilenames.append(fullfilename)
    for fullfilename in filtererd_fullfilenames:
        run_test_under_subprocess(fullfilename, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager.delete_test_environment()

    # queue/status/watch tests
    tests(coverage_activated=coverage_activated)

    # start/stop tests
    run_env1_download_start(coverage_activated=coverage_activated)
    run_env1_download_stop(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()
