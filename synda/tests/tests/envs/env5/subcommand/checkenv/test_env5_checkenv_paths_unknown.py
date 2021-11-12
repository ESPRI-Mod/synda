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

    Paths have not been customized by User

 Sub-command : synda check
 Context : env5
"""
import pytest

from synda.tests.manager import Manager
Manager()


@pytest.mark.on_all_envs
def test_env5_checkenv_paths_unknown(env5_checkenv_context, capsys):

    context = env5_checkenv_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.checkenv.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
