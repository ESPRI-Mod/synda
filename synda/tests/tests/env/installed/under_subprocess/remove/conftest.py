# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import pytest

from synda.tests.manager import Manager
manager = Manager()
manager.set_tests_mode()


# COUNT SUCOMMAND

from synda.tests.context.remove.constants import ENVS
from synda.tests.context.remove.models import Context as RemoveContext


# LIST FIXTURES

@pytest.fixture
def remove_dataset_context():
    context = RemoveContext()
    return context


def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    source = ENVS["installed"]["env"]["full_filename"]
    manager.create_test_environment(source=source)


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    manager.delete_test_environment()
