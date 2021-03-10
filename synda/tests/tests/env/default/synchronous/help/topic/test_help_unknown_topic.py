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
 Optional argument : help
 Operating context : Topic not found
"""
import sys
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.sdt import main as synda


@pytest.mark.on_all_envs
def test_help_unknown_topic(capsys):

    from synda.tests.stderr import HELP_UNKNOWN_TOPIC
    sys.argv = ['synda', "help", "unknown topic"]

    with pytest.raises(BaseException) as exception:
        synda.run()
    assert exception.value.code in [0]

    captured = capsys.readouterr()
    assert captured.err == "{}\n".format(
        HELP_UNKNOWN_TOPIC,
    )
