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

from sdt.tests.file.models import File
from sdt.tests.file.context.models import get_checksum

from sdt.tests.file.checksum.models import Checksum
from sdt.tests.file.context.models import Filename

from sdt.tests.subcommand.get import ByFilenameAndConfigFile as SubCommand


def build():

    dataset = "cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601"

    # The dataset used for the test contains the 3 following files

    filenames = [
        "areacella_fx_CanCM4_decadal1972_r0i0p0.nc",
        "orog_fx_CanCM4_decadal1972_r0i0p0.nc",
        "sftlf_fx_CanCM4_decadal1972_r0i0p0.nc",
    ]

    checksum_type = "sha256"

    folder = os.path.join(
        os.environ["ST_HOME"],
    )

    get_checksum(filename, folder, checksum_type)



    expected_filenames_and_checksums = get_expected_filenames_and_checksums(checksum_type)

    filename = "cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601"

    expected_checksum_value = "39a8e81cdadb6c1a2a38088e080d14898cfc6270b2c90419c0d1d96e771dde30"

    dest_folder = os.path.join(
        os.environ["ST_HOME"],
        "sandbox",
    )

    context = Filename(
        expected_filenames_and_checksums,
        dest_folder,
        create_folder=True,
    )

    sub_command = SubCommand(context)

    sub_command.execute()


if __name__ == '__main__':
    build()
