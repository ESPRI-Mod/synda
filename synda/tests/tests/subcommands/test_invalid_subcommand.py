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

 Sub-command : -
 Operating context : Invalid sub command
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.bin import main as synda


@pytest.mark.on_all_envs
def test_invalid_subcommand():

    sys.argv = ['synda', "x"]

    with pytest.raises(BaseException) as exception:
        synda.run()

    # it's the parser.parse_args() method that raises this code exit(2)
    # => an stderr is also displayed : "usage: synda [-h] [-V] subcommand ...
    # synda: error: argument subcommand: invalid choice: 'x' (choose from 'autoremove', and so on"

    assert exception.value.code == 2
