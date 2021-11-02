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

 Sub-command : COUNT
 Positional argument : datanode used for tests
 Operating context : retrieves the number of files
"""
import pytest


@pytest.mark.on_all_envs
def test_env1_count_files(count_vesgint_files_context, capsys):

    context = count_vesgint_files_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.api.esgf_search.count.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
