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
 Positional argument : stop
 Operating context :
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()


@pytest.mark.on_all_envs
def test_daemon_stop(stop_daemon, capsys):
    context = stop_daemon

    context.set_capsys(capsys)

    from synda.tests.subcommand.daemon.stop.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()


if __name__ == '__main__':
    test_daemon_start()
