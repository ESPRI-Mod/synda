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

 Sub-command : REMOVE
 Positional argument : a dataset name
 Operating context :  synchronous
"""
import pytest

from synda.tests.manager import Manager
Manager()


@pytest.mark.on_all_envs
def test_remove_dataset(remove_dataset_context, capsys):

    context = remove_dataset_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.remove.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
