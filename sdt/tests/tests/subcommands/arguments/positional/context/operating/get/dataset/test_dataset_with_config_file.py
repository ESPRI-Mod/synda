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
 Positional argument : filename
 Operating context :  downloading local path given by config file
"""
import os
import pytest


from sdt.tests.context.get.dataset.models import Context
from sdt.tests.subcommand.get.dataset.models import ConfigFileSubCommand as SubCommand


@pytest.mark.on_all_envs
def test_dataset_with_config_file(capsys):

    dataset = "cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601"

    dest_folder = os.path.join(
        os.environ["ST_HOME"],
        "sandbox",
    )

    context = Context(
        dataset,
        dest_folder,
        capsys=capsys,
    )

    sub_command = SubCommand(context)

    sub_command.execute()
