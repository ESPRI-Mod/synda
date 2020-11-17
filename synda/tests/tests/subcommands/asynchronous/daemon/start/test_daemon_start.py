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

 Sub-command : DAEMON
 Positional argument : start
 Operating context :
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.subcommand.asynchronous.processes import SubCommandExecute as Process



@pytest.mark.on_all_envs
def test_daemon_start(start_daemon, capsys):
    context = start_daemon

    context.set_capsys(capsys)

    from synda.tests.subcommand.daemon.start.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    process = Process(sub_command)
    process.start()


if __name__ == '__main__':
    test_daemon_start()
