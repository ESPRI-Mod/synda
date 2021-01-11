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
 Operating context :  subprocess downloading (local path given by config file)
"""
import os
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.tests.config.file.input.confirm.update.constants import CREDENTIALS as CONFIRM_UPDATE_CREDENTIALS_FILE
from synda.tests.tests.constants import ST_HOME_TESTS
from synda.tests.file.models import File
from synda.tests.file.expected.models import Description


@pytest.mark.on_all_envs
def test_filename(install_filename_context, capsys):

    context = install_filename_context

    filename = \
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.rcp85.fx.atmos.fx.r0i0p0.v20130826.sftlf_fx_CNRM-CM5_rcp85_r0i0p0.nc"

    dest_folder = os.path.join(
        ST_HOME_TESTS,
        "sandbox",
    )

    context.set_file(filename, dest_folder=dest_folder)
    context.set_capsys(capsys)

    # context.set_expected_files_description(
    #     Description(
    #         [
    #             File(
    #                 "orog_fx_CanCM4_decadal1972_r0i0p0.nc",
    #                 dest_folder,
    #             ),
    #             File(
    #                 "orog_fx_CanCM4_decadal1972_r0i0p0.nc",
    #                 dest_folder,
    #             ),
    #             File(
    #                 "sftlf_fx_CanCM4_decadal1972_r0i0p0.nc",
    #                 dest_folder,
    #             ),
    #         ],
    #     ),
    # )

    from synda.tests.subcommand.install.filename.models import SubCommand

    sub_command = SubCommand(context, exceptions_codes=[0])
    # sys.stdin = open(CONFIRM_UPDATE_CREDENTIALS_FILE)

    sub_command.execute()
    pass


if __name__ == '__main__':
    test_filename()
