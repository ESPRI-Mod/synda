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
 Optional argument : selection_file
 Operating context :
"""
import os
import pytest

from sdt.tests.manager import Manager
Manager().set_tests_mode()

from sdt.tests.constants import DATADIR, ST_HOME_TESTS
from sdt.tests.file.models import File
from sdt.tests.file.expected.models import Description


@pytest.mark.on_all_envs
def test_data(get_selection_context, capsys):

    context = get_selection_context

    selection_file = os.path.join(
        DATADIR,
        "test_selection_downloading_some_data.txt",
    )

    dest_folder = os.path.join(
        ST_HOME_TESTS,
        "data",
    )

    context.set_selection_file(selection_file)
    context.set_folder(dest_folder)

    context.set_capsys(capsys)

    context.set_expected_files_description(
        Description(
            [
                File(
                    "psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc",
                    dest_folder,
                ),
            ],
        ),
    )

    from sdt.tests.subcommand.get.selection.models import SelectionGetSubCommand as SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
