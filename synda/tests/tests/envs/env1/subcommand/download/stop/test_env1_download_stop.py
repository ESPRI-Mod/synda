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

 Sub-command             : synda download stop
 Name of synda workspace : env1
"""
import os
import pytest


from synda.tests.tests.envs.env1.constants import TESTS_DIR


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def get_test_download_start_fullfilename():
    dirname = os.path.join(
        get_subcommand_dirname("download"),
        "stop",
    )

    fullfilename = os.path.join(
        dirname,
        "test_env1_download_start.py",
    )

    return fullfilename


@pytest.mark.on_all_envs
def test_env1_download_stop(env1_download_stop_context, capsys):
    context = env1_download_stop_context

    context.set_capsys(capsys)

    from synda.tests.subcommand.download.stop.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])

    sub_command.execute()
