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

 Sub-command : DAEMON
 Positional argument : start
 Operating context :
"""
import sys
import pytest

from sdt.bin import synda
from sdt.bin.sdi18n import m0028


@pytest.mark.on_all_envs_disabled
def test_daemon_start(capsys):

    sys.argv = ['synda', "daemon", "start"]

    with pytest.raises(BaseException) as exception:
        synda.run()
    assert exception.value.code in [0, 1]

    captured = capsys.readouterr()
    assert captured.err == "{}\n".format(
        m0028,
    )
