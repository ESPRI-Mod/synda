# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import pytest

# DAEMON SUCOMMAND

from sdt.tests.context.daemon.start.models import Context as StartDaemonContext
from sdt.tests.context.daemon.stop.models import Context as StopDaemonContext

# DAEMON FIXTURES


@pytest.fixture()
def start_daemon():
    return StartDaemonContext()


@pytest.fixture()
def stop_daemon():
    return StopDaemonContext()
