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

 Sub-command : synda download queue
 Context : env0
"""
import pytest


@pytest.mark.on_all_envs
def test_env0_download_queue(env0_download_queue_context, capsys):

    context = env0_download_queue_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.download.queue.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
