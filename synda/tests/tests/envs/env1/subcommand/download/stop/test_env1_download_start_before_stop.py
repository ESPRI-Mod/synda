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

 Sub-command             : synda download start
 Name of synda workspace : env1
"""
import pytest


@pytest.mark.on_all_envs
def test_env1_download_start_before_stop(env1_download_stop_context, capsys):

    context = env1_download_stop_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.download.start.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
