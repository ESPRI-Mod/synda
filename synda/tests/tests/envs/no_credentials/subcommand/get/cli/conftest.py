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

from synda.tests.context.envs.no_credentials.constants import ENV
from synda.tests.context.envs.no_credentials.subcommand.get.cli.openid.default.models \
    import Context as FilenameCliDefaultOpenidContext
from synda.tests.context.envs.no_credentials.subcommand.get.cli.openid.unknown.models \
    import Context as FilenameCliUnknownOpenidContext
from synda.tests.context.envs.no_credentials.subcommand.get.cli.password.unknown.models \
    import Context as FilenameCliUnknownPasswordContext

# FIXTURES

@pytest.fixture
def env0_get_filename_cli_default_openid_context():

    context = FilenameCliDefaultOpenidContext()
    return context

@pytest.fixture
def env0_get_filename_cli_unknown_openid_context():

    context = FilenameCliUnknownOpenidContext()
    return context


@pytest.fixture
def env0_get_filename_cli_unknown_password_context():

    context = FilenameCliUnknownPasswordContext()
    return context

def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    source = ENV["full_filename"]
    manager.create_test_environment(source=source, with_credentials=False)

# FIXTURE CALLED AFTER EACH TEST

def pytest_runtest_teardown(item):
    manager.delete_test_environment()
