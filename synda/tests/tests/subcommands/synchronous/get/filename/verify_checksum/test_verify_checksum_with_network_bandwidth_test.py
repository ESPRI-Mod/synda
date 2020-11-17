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
 Optional argument : verify_checksum
 Parsing context : verify_checksum and network_bandwidth_test
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.bin import main as synda
from synda.tests.stderr import NETWORK_BANDWIDTH_TEST


@pytest.mark.on_all_envs
def test_verify_checksum_with_network_bandwidth_test(capsys):

    filename = "orog_fx_CanCM4_decadal1972_r0i0p0.nc"

    sys.argv = ['', "get", "--verify_checksum", "--network_bandwidth_test", filename]

    with pytest.raises(BaseException) as exception:
        synda.run()
    assert exception.value.code in [1]

    captured = capsys.readouterr()
    assert "{}".format(
        NETWORK_BANDWIDTH_TEST,
    ) in captured.err
