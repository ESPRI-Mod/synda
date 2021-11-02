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

 Sub-command : synda version
 Context : env0
"""
import pytest

from synda.tests.manager import Manager
Manager()


from synda.tests.tests.constants import DATASET_EXAMPLE


@pytest.mark.on_all_envs
def test_env0_version(env0_version_context, capsys):

    context = env0_version_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.version.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
