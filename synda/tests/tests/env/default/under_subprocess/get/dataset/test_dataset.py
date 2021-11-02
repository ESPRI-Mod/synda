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
import os
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()


from synda.tests.tests.constants import ST_HOME_TESTS
from synda.tests.file.models import File
from synda.tests.file.expected.models import Description

from synda.tests.tests.constants import DATASET_EXAMPLE


@pytest.mark.on_all_envs
def test_dataset(get_dataset_context, capsys):

    context = get_dataset_context

    dataset_name = DATASET_EXAMPLE["name"]

    dest_folder = os.path.join(
        ST_HOME_TESTS,
        "sandbox",
    )
    context.set_dataset(dataset_name, dest_folder=dest_folder)
    context.set_capsys(capsys)

    context.set_expected_files_description(
        Description(
            [
                File(
                    DATASET_EXAMPLE["files"][0],
                    dest_folder,
                ),
                File(
                    DATASET_EXAMPLE["files"][1],
                    dest_folder,
                ),
                File(
                    DATASET_EXAMPLE["files"][2],
                    dest_folder,
                ),
            ],
        ),
    )

    from synda.tests.subcommand.get.dataset.models import DestFolderSubCommand as SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
