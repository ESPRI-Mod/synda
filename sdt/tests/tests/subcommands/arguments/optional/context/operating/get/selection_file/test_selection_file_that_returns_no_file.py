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
 Operating context :
"""
import os
import sys
import pytest

from sdt.tests.constants import DATADIR
from sdt.tests.stderr import FILE_NOT_FOUND

from sdt.bin import synda


@pytest.mark.on_all_envs
def test_selection_file_that_returns_no_file(capsys):

    selection_file = os.path.join(
        DATADIR,
        "test_selection_downloading_no_data.txt",
    )

    sys.argv = ['synda', "get", "--selection_file", selection_file]

    with pytest.raises(BaseException) as exception:
        synda.run()

    assert exception.value.code == 1

    captured = capsys.readouterr()
    assert captured.err == "{}\n".format(
        FILE_NOT_FOUND,
    )
