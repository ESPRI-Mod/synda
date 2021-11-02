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
 Operating context :  downloading local path given by positional argument --dest_folder
"""
import os
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.tests.constants import ST_HOME_TESTS
from synda.tests.file.models import File
from synda.tests.file.expected.models import Description


@pytest.mark.on_all_envs
def test_filename(get_filename_context, capsys):

    context = get_filename_context

    filename = "orog_fx_CanCM4_decadal1972_r0i0p0.nc"

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

    from synda.tests.subcommand.get.filename.models import DestFolderGetSubCommand as SubCommand

    sub_command = SubCommand(context, exceptions_codes=[1])

    sub_command.execute()
