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

from synda.tests.context.envs.env0.constants import ENV
from synda.tests.context.envs.env0.subcommand.get.filename.models import BasicContext
from synda.tests.context.envs.env0.subcommand.get.filename.models \
    import VerifyChecksumContext

from synda.tests.context.envs.env0.subcommand.get.filename.models \
    import VerifyChecksumWithNetworkBandwidthTestContext

# FIXTURES

@pytest.fixture
def env0_get_file_context_dest_folder():
    context = BasicContext()
    return context

@pytest.fixture
def env0_get_file_context_dest_folder_verify_checksum():
    context = VerifyChecksumContext()
    return context

@pytest.fixture
def env0_get_file_context_dest_folder_verify_checksum_with_network_bandwidth_test():
    context = VerifyChecksumWithNetworkBandwidthTestContext()
    return context

def pytest_collection_modifyitems(session, config, items):
    manager.delete_test_environment()


def pytest_runtest_setup(item):
    source = ENV["full_filename"]
    manager.create_test_environment(source=source)

# FIXTURE CALLED AFTER EACH TEST

def pytest_runtest_teardown(item):
    manager.delete_test_environment()
