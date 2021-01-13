# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import time

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.tests.stderr import FILE_NOT_FOUND
from synda.tests.context.external_storage.models import Context as Base


class Context(Base):

    def validation_after_subcommand_execution(self):
        pass

        # from sdt.bin import sdconfig
        # print "EXPECTED PID FILE LOCATION = {}".format(sdconfig.daemon_pid_file)
        # assert os.path.isfile(sdconfig.daemon_pid_file)
        #
        # i = 0
        # imax = 40
        # eod = False
        # while i < imax and not eod:
        #     if os.path.isfile(sdconfig.daemon_pid_file):
        #         eod = True
        #     time.sleep(5)
        #     i += 1
        #
        # if i >= imax:
        #     assert False
        # else:
        #     assert False
