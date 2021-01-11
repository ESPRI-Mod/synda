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
 Operating context : file doesn't exist
"""
import sys
import pytest

from synda.tests.manager import Manager
from synda.source.process.env.manager import Manager as EnvManager

Manager().set_tests_mode()
from synda.tests.tests.config.file.input.confirm.update.constants import CREDENTIALS as CONFIRM_UPDATE_CREDENTIALS_FILE


@pytest.mark.on_all_envs
def test_init_env_context(init_env_context, check_env_context, capsys):
    context = init_env_context
    context.set_capsys(capsys)

    env_manager = EnvManager()
    env_manager.init(interactive_mode=False)

    # control with  'check-env'

    context = check_env_context
    context.set_capsys(capsys)

    from synda.tests.subcommand.checkenv.models import SubCommand
    sys.stdin = open(CONFIRM_UPDATE_CREDENTIALS_FILE)
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
