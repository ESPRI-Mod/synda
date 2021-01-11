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


def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    manager.create_test_environment()


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    manager.delete_test_environment()
