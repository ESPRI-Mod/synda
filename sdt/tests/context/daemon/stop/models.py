# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from time import sleep

from sdt.tests.manager import Manager
Manager().set_tests_mode()

from sdt.tests.constants import WAIT_DURATION_AFTER_DAEMON_STOP
from sdt.tests.context.external_storage.models import Context as Base


class Context(Base):

    def validation_after_subcommand_execution(self):
        print "Control that the status of the daemon is : 'stopped'..."
        from sdt.tests.manager import Manager
        Manager().set_tests_mode()
        from sdt.bin import sddaemon

        sleep(WAIT_DURATION_AFTER_DAEMON_STOP)
        assert not sddaemon.is_running()
