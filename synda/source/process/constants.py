# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import sys


def is_daemon():

    # the parent of a daemon is always Init, so check for ppid 1
    if os.getppid() == 1:

        # note that in some case, some non-daemon also have init as parent
        # so we double check with controlling tty (i.e. daemon have no controlling tty)
        if not os.isatty(sys.stdout.fileno()):
            return True
        else:
            return False

    else:
        return False
