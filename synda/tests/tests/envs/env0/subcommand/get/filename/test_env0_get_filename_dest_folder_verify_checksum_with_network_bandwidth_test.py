# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Tests driven by pytest

 Sub-command : GET
 Positional argument : filename
 Operating context :  downloading local path given by config file
"""
import sys
import os
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()


from synda.tests.tests.constants import ST_HOME_TESTS
from synda.tests.file.models import File
from synda.tests.file.expected.models import Description

from synda.tests.context.envs.constants import SYNDA_DEV_DATA
from synda.tests.context.envs.env0.constants import SUBCOMMAND_GET_CONFIRM_ANSWER_FILE


@pytest.mark.on_all_envs
def test_env0_get_filename_dest_folder_verify_checksum_with_network_bandwidth_test(
        env0_get_file_context_dest_folder_verify_checksum_with_network_bandwidth_test,
        capsys,
):

    context = env0_get_file_context_dest_folder_verify_checksum_with_network_bandwidth_test

    filename = SYNDA_DEV_DATA["cordex"]["files"][0]

    dest_folder = os.path.join(
        ST_HOME_TESTS,
        "sandbox",
    )
    context.set_file(filename, dest_folder=dest_folder)
    context.set_capsys(capsys)

    context.set_expected_files_description(
        Description(
            [
                File(
                    filename,
                    dest_folder,
                ),
            ],
        ),
    )

    from synda.tests.subcommand.get.filename.models import VerifyChecksumWithNetworkBandwidthTestSubCommand as SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])
    sys.stdin = open(SUBCOMMAND_GET_CONFIRM_ANSWER_FILE)
    sub_command.execute()
