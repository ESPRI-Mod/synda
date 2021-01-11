# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.manager import Manager
manager = Manager()
manager.set_tests_mode()

from synda.tests.tests.utils import run_simple_tests
from synda.tests.tests.utils import search_requested_fullfilenames
from synda.tests.tests.config.constants import TESTS_DIR


def main():

    manager.set_tests_mode()
    manager.create_test_environment()

    fullfilenames = search_requested_fullfilenames(
        TESTS_DIR,
    )

    run_simple_tests(fullfilenames)
    manager.delete_test_environment()


if __name__ == '__main__':
    main()

