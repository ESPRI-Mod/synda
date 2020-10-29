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
 Operating context :  downloading local path given by positional argument --dest_folder
"""
import os
import pytest

from sdt.tests.file.checksum.models import Checksum

from sdt.tests.context.get.filename.models import Context
from sdt.tests.subcommand.get.filename.models import DestFolderGetSubCommand as SubCommand


@pytest.mark.on_all_envs
def test_filename_with_dest_folder(capsys):

    filename = "orog_fx_CanCM4_decadal1972_r0i0p0.nc"

    checksum = Checksum()

    dest_folder = os.path.join(
        os.path.join(
            os.environ["ST_HOME"],
            "sandbox",
        ),
        "tmp",
    )

    context = Context(
        filename,
        dest_folder,
        capsys=capsys,
    )

    sub_command = SubCommand(context)

    sub_command.execute()
