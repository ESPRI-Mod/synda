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

 Sub-command : INSTALL
 Positional argument : filename
 Operating context :  asynchronous downloading (local path given by config file)
"""
import os
import pytest

from sdt.tests.context.get.filename.models import Context
from sdt.tests.subcommand.install.filename.models import SubCommand


@pytest.mark.on_all_envs
def test_filename(capsys):

    filename = \
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.rcp85.fx.atmos.fx.r0i0p0.v20130826.sftlf_fx_CNRM-CM5_rcp85_r0i0p0.nc"

    dest_folder = os.path.join(
        os.environ["ST_HOME"],
        "sandbox",
    )

    context = Context(
        filename,
        dest_folder,
        capsys=capsys,
    )

    sub_command = SubCommand(context)

    sub_command.execute()
