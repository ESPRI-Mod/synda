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
 Positional argument : url
 Operating context :  credentials not set
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.context.envs.constants import SYNDA_DEV_DATA
from synda.tests.context.envs.env0.constants import SUBCOMMAND_GET_CONFIRM_ANSWER_FILE


@pytest.mark.on_all_envs
def test_env0_get_filename_config_unknown_password(env0_get_filename_config_unknown_password_context, capsys):

    context = env0_get_filename_config_unknown_password_context

    filename = SYNDA_DEV_DATA["cordex"]["files"][0]

    context.set_file(filename)
    context.set_capsys(capsys)

    from synda.tests.subcommand.get.filename.no_credentials.config.password.unknown.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])
    sys.stdin = open(SUBCOMMAND_GET_CONFIRM_ANSWER_FILE)
    sub_command.execute()
