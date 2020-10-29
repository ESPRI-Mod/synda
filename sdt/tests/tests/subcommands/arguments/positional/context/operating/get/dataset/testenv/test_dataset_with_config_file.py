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

from sdt.tests.constants import DATADIR

from sdt.tests.file.checksum.models import Checksum
from sdt.tests.file.expected.reader import Reader

from sdt.tests.context.get.dataset.models import TestEnvContext as Context

from sdt.tests.subcommand.get.dataset.models import ConfigFileSubCommand as SubCommand


@pytest.mark.on_test_env
def test_by_dataset_and_config_file(capsys):

    checksum_type = "sha256"

    dataset = "cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601"

    folder = os.path.join(
        DATADIR,
        "testenv",
    )

    reader = Reader(
        os.path.join(
            folder,
            "test_by_dataset_and_config_file.txt",
        ),
    )

    filenames = reader.get_index()

    expected_files_description = dict()
    for filename in filenames:
        checksum = Checksum(
            checksum_type,
            reader.get_checksum(filename),
        )
        expected_files_description[filename] = checksum

    dest_folder = os.path.join(
        os.environ["ST_HOME"],
        "sandbox",
    )

    context = Context(
        dataset,
        dest_folder,
        expected_files_description=expected_files_description,
        capsys=capsys,
    )

    sub_command = SubCommand(context)

    sub_command.execute()
