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

 Sub-command : VERSION
 Positional argument : a dataset name
 Operating context :  synchronous
"""
import os
import pytest

from synda.tests.manager import Manager
Manager()


from synda.tests.tests.constants import DATASET_EXAMPLE


@pytest.mark.on_all_envs
def test_dataset(version_context, capsys):

    context = version_context

    dataset_name = DATASET_EXAMPLE["name"]

    context.set_dataset(dataset_name)
    context.set_capsys(capsys)

    from synda.tests.subcommand.version.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
