# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import pytest

# GET SUCOMMAND

from synda.tests.context.download.filename.models import Context as GetFilenameContext
from synda.tests.context.download.dataset.models import Context as GetDatasetContext

from synda.tests.context.download.selection.no_data.models import Context as GetSelectionDataNotFoundContext
from synda.tests.context.download.selection.models import Context as GetSelectionContext

# INSTALL SUCOMMAND

from synda.tests.context.download.install.filename.models import Context as InstallFilenameContext

# DAEMON SUCOMMAND

from synda.tests.context.daemon.start.models import Context as StartDaemonContext
from synda.tests.context.daemon.stop.models import Context as StopDaemonContext

# COUNT SUCOMMAND

from synda.tests.context.api.esgf_search.count.usercase.cmip5.dataset.models import Context as \
    CountDatasetsContextForCmip5UserCase

from synda.tests.context.api.esgf_search.count.usercase.cmip5.file.models import Context as \
    CountFilesContextForCmip5UserCase


# SEARCH SUCOMMAND

from synda.tests.context.api.esgf_search.search.dataset.models import Context as DatasetSearchContext
from synda.tests.context.api.esgf_search.search.file.models import Context as FileSearchContext


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
def count_datasets_context_for_cmip5_usercase():
    context = CountDatasetsContextForCmip5UserCase()
    return context


@pytest.fixture
def count_files_context_for_cmip5_usercase():
    context = CountFilesContextForCmip5UserCase()
    return context

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


# DAEMON FIXTURES


@pytest.fixture()
def start_daemon():
    return StartDaemonContext()


@pytest.fixture()
def stop_daemon():
    return StopDaemonContext()
