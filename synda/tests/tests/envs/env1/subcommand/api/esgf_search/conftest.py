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

from synda.tests.context.envs.env1.constants import ENV

# COUNT SUCOMMAND

from synda.tests.context.envs.env1.subcommand.api.esgf_search.count.datanode.vesgint.dataset.models \
    import Context as CountVesgintDatasetsContext

from synda.tests.context.envs.env1.subcommand.api.esgf_search.count.datanode.vesgint.file.models \
    import Context as CountVesgintFilesContext

# SEARCH SUCOMMAND

from synda.tests.context.envs.env1.subcommand.api.esgf_search.search.dataset.models \
    import Context as DatasetSearchContext
from synda.tests.context.envs.env1.subcommand.api.esgf_search.search.file.models \
    import Context as FileSearchContext


# SEARCH FIXTURE

@pytest.fixture
def dataset_search_context():
    context = DatasetSearchContext()
    return context


@pytest.fixture
def file_search_context():
    context = FileSearchContext()
    return context


# COUNT FIXTURE

@pytest.fixture
def count_vesgint_datasets_context():
    context = CountVesgintDatasetsContext()
    return context


@pytest.fixture
def count_vesgint_files_context():
    context = CountVesgintFilesContext()
    return context


def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    source = ENV["full_filename"]
    manager.create_test_environment(source=source)


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    manager.delete_test_environment()
