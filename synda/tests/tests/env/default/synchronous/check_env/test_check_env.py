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
import os
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.utils import has_environment_variable

from synda.source.process.env.check.models import Config
from synda.source.config.env.check.constants import ERROR_ENVIRONMENT_VARIABLE_PREFIX
from synda.tests.tests.config.file.input.confirm.update.constants import CREDENTIALS as CONFIRM_UPDATE_CREDENTIALS_FILE


@pytest.mark.on_all_envs
def test_var_env():
    assert has_environment_variable(var_name='ST_HOME')


@pytest.mark.on_all_envs
def test_location_exists():
    assert os.path.isdir(os.environ['ST_HOME'])


@pytest.mark.on_all_envs
def test_not_ok(capsys):
    root = ""
    config = Config(root)

    config.process()

    captured = capsys.readouterr()
    assert ERROR_ENVIRONMENT_VARIABLE_PREFIX in captured.out


@pytest.mark.on_all_envs
def test_one_required_file_missing(one_required_file_missing_check_env_context, capsys):
    context = one_required_file_missing_check_env_context
    context.set_capsys(capsys)

    from synda.tests.subcommand.checkenv.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()


@pytest.mark.on_all_envs
def test_one_required_directory_missing(one_required_directory_missing_check_env_context, capsys):
    context = one_required_directory_missing_check_env_context
    context.set_capsys(capsys)

    from synda.tests.subcommand.checkenv.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()


@pytest.mark.on_all_envs
def test_ok(check_env_context, capsys):
    context = check_env_context
    context.set_capsys(capsys)

    from synda.tests.subcommand.checkenv.models import SubCommand
    sub_command = SubCommand(context, exceptions_codes=[0])
    sys.stdin = open(CONFIRM_UPDATE_CREDENTIALS_FILE)
    sub_command.execute()
