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

from synda.tests.context.envs.env1.constants import ENV
from synda.tests.context.envs.env1.subcommand.api.esgf_search.list.dataset.models import Context as DatasetListContext
from synda.tests.context.envs.env1.subcommand.api.esgf_search.list.file.models import Context as FileListContext


# LIST FIXTURES

@pytest.fixture
def dataset_list_context():
    context = DatasetListContext()
    return context


@pytest.fixture
def file_list_context():
    context = FileListContext()
    return context


def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    source = ENV["full_filename"]
    manager.create_test_environment(source=source)


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    manager.delete_test_environment()
