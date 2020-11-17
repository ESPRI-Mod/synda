# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import re
from time import sleep
import pytest
import subprocess

from synda.tests.constants import ASYNCHRONOUS_SUBCOMMANDS_DIR
from synda.tests.constants import WAIT_DURATION_AFTER_DAEMON_START
from synda.tests.manager import Manager


def get_subcommand_dirname(subcommand):
    return os.path.join(
        ASYNCHRONOUS_SUBCOMMANDS_DIR,
        subcommand,
    )


def get_pytest_source_fullfilename():
    candidate = pytest.__file__
    regex = ".py$"
    match = re.search(regex, candidate)
    if match:
        fullfilename = candidate
    else:
        regex = ".pyc$"
        match = re.search(regex, candidate)
        if match:
            fullfilename= candidate.replace(".pyc", ".py")
        else:
            fullfilename = ""

    return fullfilename


def get_test_daemon_fullfilename(arg):
    dirname = os.path.join(
        get_subcommand_dirname("daemon"),
        "{}".format(arg),
    )

    fullfilename = os.path.join(
        dirname,
        "test_daemon_{}.py".format(arg),
    )

    return fullfilename


def run_test(fullfilename):
    print "Testing : {}".format(fullfilename)
    subprocess.call(
        ["python", get_pytest_source_fullfilename(), "-v", "-m", "on_all_envs", "-x", fullfilename],
    )


def test_start_daemon():

    Manager().create_test_environment()

    fullfilename = get_test_daemon_fullfilename("start")

    # STEP 1 : start the daemon

    run_test(fullfilename)

    # Wait for 'WAIT_DURATION_AFTER_DAEMON_START' seconds to be sure that the daemon is running

    sleep(WAIT_DURATION_AFTER_DAEMON_START)

    # STEP 2 : control that the status of the daemon is : "running"

    subprocess.call(
        [
            'python',
            os.path.join(
                os.path.join(
                    os.path.join(
                        get_subcommand_dirname("daemon"),
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
    run_test(fullfilename)

    Manager().delete_test_environment()


def main():

    Manager().delete_test_environment()

    test_start_daemon()


if __name__ == '__main__':
    main()

