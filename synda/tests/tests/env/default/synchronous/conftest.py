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

# # GET SUCOMMAND
#
# from synda.tests.context.download.filename.models import Context as GetFilenameContext
# from synda.tests.context.download.dataset.models import Context as GetDatasetContext
#
# from synda.tests.context.download.selection.no_data.models import Context as GetSelectionDataNotFoundContext
# from synda.tests.context.download.selection.models import Context as GetSelectionContext

# CHECK-ENV SUCOMMAND

from synda.tests.context.env.check.models import Context as CheckEnvContext
from synda.tests.context.env.check.models import OneRequiredFileMissingContext as OneRequiredFileMissingCheckEnvContext
from synda.tests.context.env.check.models import \
    OneRequiredDirectoryMissingContext as OneRequiredDirectoryMissingCheckEnvContext

# VERSION SUCOMMAND

from synda.tests.context.version.models import Context as VersionContext


# VERSION FIXTURE


@pytest.fixture
def version_context():
    context = VersionContext()
    return context


# CHECK-ENV FIXTURES


@pytest.fixture
def check_env_context():
    context = CheckEnvContext()
    return context


@pytest.fixture
def one_required_file_missing_check_env_context():
    context = OneRequiredFileMissingCheckEnvContext()
    return context


@pytest.fixture
def one_required_directory_missing_check_env_context():
    context = OneRequiredDirectoryMissingCheckEnvContext()
    return context


def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    manager.create_test_environment()


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    manager.delete_test_environment()
