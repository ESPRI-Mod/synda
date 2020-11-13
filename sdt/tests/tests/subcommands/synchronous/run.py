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
import pytest

from sdt.tests.constants import SYNCHRONOUS_SUBCOMMANDS_DIR


def get_subcommand_dirname(subcommand):
    return os.path.join(
        SYNCHRONOUS_SUBCOMMANDS_DIR,
        subcommand,
    )


def is_test_filename(filename):
    regex = "^test_.*.py$"
    match = re.search(regex, filename)
    return True if match else False


def search_requested_fullfilenames(dirname):
    fullfilenames = []
    for dirpath, subdirectories, filenames in os.walk(dirname):
        for filename in filenames:
            if is_test_filename(filename):
                fullfilenames.append(
                    os.path.join(
                        dirpath,
                        filename,
                    ),
                )
    return fullfilenames


def run_tests(fullfilenames):
    for f in fullfilenames:
        print "Testing : {}".format(f)
        pytest.main(["-v", "-m", "on_all_envs", "-x", f])  # --maxfail=1


def main():

    # Synchronous MODE, subcommand install (except the part of the process handled by the daemon)

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("install"),
    )

    run_tests(fullfilenames)

    # Synchronous MODE, subcommand autoremove

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("autoremove"),
    )

    run_tests(fullfilenames)

    # Synchronous MODE, subcommand get

    fullfilenames = search_requested_fullfilenames(
        get_subcommand_dirname("get"),
    )

    run_tests(fullfilenames)


if __name__ == '__main__':
    main()

