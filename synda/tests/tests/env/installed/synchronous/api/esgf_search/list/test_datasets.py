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

 Sub-command : LIST
 Positional argument : a project name
 Operating context :  retrieves the number of datasets
"""
import pytest


@pytest.mark.on_all_envs
def test_datasets(dataset_list_context, capsys):

    context = dataset_list_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.api.esgf_search.list.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
