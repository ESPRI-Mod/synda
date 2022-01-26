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

from synda.tests.context.envs.no_credentials.subcommand.get.config.password.unknown.constants import ENV
from synda.tests.context.envs.no_credentials.subcommand.get.config.password.unknown.models \
    import Context as UnknownPasswordContext

# FIXTURES

@pytest.fixture
def env0_get_filename_config_unknown_password_context():
    context = UnknownPasswordContext()
    return context

def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    source = ENV["full_filename"]
    manager.create_test_environment(source=source, with_credentials=False)

# FIXTURE CALLED AFTER EACH TEST

def pytest_runtest_teardown(item):
    manager.delete_test_environment()
