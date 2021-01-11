# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import pytest

from synda.tests.manager import Manager
manager = Manager()
manager.set_tests_mode()

# INIT-ENV SUCOMMAND

from synda.tests.context.env.init.models import Context as InitEnvContext

# CHECK-ENV SUCOMMAND

from synda.tests.context.env.check.models import Context as CheckEnvContext

# INIT-ENV FIXTURE


@pytest.fixture
def init_env_context():
    context = InitEnvContext()
    return context


@pytest.fixture
def check_env_context():
    context = CheckEnvContext()
    return context


def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


# FIXTURE CALLED AFTER EACH TEST


def pytest_runtest_teardown(item):
    manager.delete_test_environment()
