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
 Parsing context : with positional argument
"""
import os
import sys
import pytest

from sdt.tests.manager import Manager
Manager().set_tests_mode()

from sdt.bin import synda
from sdt.bin.sdexception import SDException
from sdt.tests.constants import DATADIR


@pytest.mark.on_all_envs
def test_with_parameter():

    filename = "orog_fx_CanCM4_decadal1972_r0i0p0.nc"

    selection_file = os.path.join(
        DATADIR,
        "test_selection_01.txt",
    )

    sys.argv = ['', "get", "--selection_file", selection_file, filename]

    with pytest.raises(SDException) as exception:
        synda.run()

    assert exception.value.code == 'SDBUFFER-001'
