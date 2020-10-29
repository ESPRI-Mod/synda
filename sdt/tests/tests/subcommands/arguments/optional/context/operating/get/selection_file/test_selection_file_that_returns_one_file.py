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
 Operating context :
"""
import os
import pytest

from sdt.tests.constants import DATADIR

from sdt.tests.file.checksum.models import Checksum
from sdt.tests.context.get.selection.models import Context

from sdt.tests.subcommand.get.selection.models import SelectionGetSubCommand as SubCommand


@pytest.mark.on_all_envs
def test_selection_file_that_returns_one_file(capsys):

    filename = "psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc"

    selection_file = os.path.join(
        DATADIR,
        "test_selection_downloading_some_data.txt",
    )

    dest_folder = os.path.join(
        os.environ["ST_HOME"],
        "sandbox",
    )

    context = Context(
        selection_file,
        dest_folder,
        capsys=capsys,
    )

    command = SubCommand(context)

    command.execute()
