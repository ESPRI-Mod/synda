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

 Sub-command : getinfo
 Positional argument : filename
 Operating context :
"""
import os
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.context.getinfo.filename.constants import CONTEXT


@pytest.mark.on_all_envs
def test_getinfo_filename(getinfo_filename_context, capsys):

    context = getinfo_filename_context

    filename = CONTEXT["filename"]

    context.set_file(filename)
    context.set_capsys(capsys)

    from synda.tests.subcommand.getinfo.filename.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
