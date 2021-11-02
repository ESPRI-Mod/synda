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

 Sub-command : SEARCH
 Operating context :  retrieves the name of datasets
"""
import pytest


@pytest.mark.on_all_envs
def test_env1_search_datasets(dataset_search_context, capsys):

    context = dataset_search_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.api.esgf_search.search.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
