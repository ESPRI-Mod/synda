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

from synda.tests.tests.constants import TESTS_DIR
from synda.tests.tests.config.run import main as run_config_tests
from synda.tests.tests.env.run import main as run_envs_tests


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


def main(coverage_activated=False):
    nb_tests = len(
        search_requested_fullfilenames(
            TESTS_DIR,
        ),
    )

    run_config_tests()
    run_envs_tests(coverage_activated=coverage_activated)

    print(
        "{} Tests Processed".format(
            nb_tests,
        ),
    )


if __name__ == '__main__':
    main(coverage_activated=False)
