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

 Sub-command : AUTOREMOVE
 Optional argument : dry_run
 Operating context : Regular user not allowed, only admin
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()


@pytest.mark.on_all_envs
def test_autoremove_dry_run_and_authorized_user(capsys):

    sys.argv = ['synda', "autoremove", "--dry_run"]

    from synda.bin import main as synda

    with pytest.raises(BaseException) as exception:
        synda.run()
    assert exception.value.code in [0, 1]

    captured = capsys.readouterr()
    assert captured.err == ""
    pass

