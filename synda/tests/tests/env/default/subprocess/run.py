# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import datetime
import subprocess

from synda.tests.tests.utils import run_test_under_subprocess
from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.env.default.subprocess.constants import TESTS_DIR
from synda.tests.context.daemon.start.constants import TIMEOUT
from synda.tests.manager import Manager
from synda.source.process.subcommand.daemon.models import is_running


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def get_test_daemon_fullfilename(arg):
    dirname = os.path.join(
        get_subcommand_dirname("synda_daemon"),
        "{}".format(arg),
    )

    fullfilename = os.path.join(
        dirname,
        "test_daemon_{}.py".format(arg),
    )

    return fullfilename


def test_daemon(manager):

    manager.create_test_environment()

    fullfilename = get_test_daemon_fullfilename("start")

    # STEP 1 : start the daemon

    run_test_under_subprocess(fullfilename)

    # Wait for 'WAIT_DURATION_AFTER_DAEMON_START' seconds to be sure that the daemon is running

    end = datetime.datetime.now() + datetime.timedelta(seconds=TIMEOUT)
    while not is_running() and end > datetime.datetime.now():
        continue
    # STEP 2 : control that the status of the daemon is : "running"

    subprocess.call(
        [
            'python',
            os.path.join(
                os.path.join(
                    os.path.join(
                        get_subcommand_dirname("synda_daemon"),
                        "start",
                    ),
                    "control",
                ),
                "is_running.py",
            ),
        ],
        # stdout=subprocess.PIPE,
    )

    # STEP 3 : stop the daemon

    fullfilename = get_test_daemon_fullfilename("stop")
    run_test_under_subprocess(fullfilename)

    manager.delete_test_environment()


def test_install_filename(manager, coverage_activated=False):

    manager.create_test_environment()

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("install"),
    )

    for fullfilename in fullfilenames:
        run_test_under_subprocess(fullfilename, coverage_activated=coverage_activated)

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager = Manager()
    manager.set_tests_mode()
    manager.delete_test_environment()

    test_daemon(manager)
    test_install_filename(manager, coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

