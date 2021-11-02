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

 Sub-command : synda variable
 Context : env1
"""
import pytest


@pytest.mark.on_all_envs
def test_env1_wind_speed_variable(env1_wind_speed_variable_context, capsys):
    context = env1_wind_speed_variable_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.variable.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()


@pytest.mark.on_all_envs
def test_env1_ph_variable(env1_ph_variable_context, capsys):
    context = env1_ph_variable_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.variable.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()


@pytest.mark.on_all_envs
def test_env1_no_variable(env1_no_variable_context, capsys):
    context = env1_no_variable_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.variable.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
