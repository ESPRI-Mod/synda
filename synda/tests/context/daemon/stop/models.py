# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.context.daemon.stop.constants import TIMEOUT
from synda.tests.context.models import Context as Base


class Context(Base):

    def validation_after_subcommand_execution(self):
        print("Control that the status of the daemon is : 'stopped'...")
        from synda.tests.manager import Manager
        Manager().set_tests_mode()
        from synda.sdt import sddaemon

        end = datetime.datetime.now() + datetime.timedelta(seconds=TIMEOUT)
        while sddaemon.is_running() and end > datetime.datetime.now():
            continue

        assert not sddaemon.is_running()
