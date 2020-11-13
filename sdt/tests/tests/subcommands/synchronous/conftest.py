# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import pytest

from sdt.tests.manager import Manager

# GET SUCOMMAND

from sdt.tests.context.download.filename.models import Context as GetFilenameContext
from sdt.tests.context.download.dataset.models import Context as GetDatasetContext

from sdt.tests.context.download.selection.no_data.models import Context as GetSelectionDataNotFoundContext
from sdt.tests.context.download.selection.models import Context as GetSelectionContext

# INSTALL SUCOMMAND

from sdt.tests.context.download.install.filename.models import Context as InstallFilenameContext

# GET FIXTURES


@pytest.fixture
def get_filename_context():
    context = GetFilenameContext()
    return context


@pytest.fixture
def get_dataset_context():
    context = GetDatasetContext()
    return context


@pytest.fixture
def get_selection_file_data_not_found_context():
    context = GetSelectionDataNotFoundContext()
    return context


@pytest.fixture
def get_selection_context():
    context = GetSelectionContext()
    return context


# INSTALL FIXTURES


@pytest.fixture
def install_filename_context():
    context = InstallFilenameContext()
    return context


def pytest_collection_modifyitems(session, config, items):
    Manager().delete_test_environment()


def pytest_runtest_setup(item):
    Manager().create_test_environment()


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    Manager().delete_test_environment()
