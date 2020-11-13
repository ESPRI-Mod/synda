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

from sdt.tests.constants import DATADIR


@pytest.mark.on_all_envs
def test_no_data(get_selection_file_data_not_found_context, capsys):

    context = get_selection_file_data_not_found_context

    selection_file = os.path.join(
        DATADIR,
        "test_selection_downloading_no_data.txt",
    )

    context.set_selection_file(selection_file)
    context.set_capsys(capsys)

    from sdt.tests.subcommand.get.selection.models import SelectionGetSubCommand as SubCommand

    sub_command = SubCommand(context, exceptions_codes=[1])

    sub_command.execute()
