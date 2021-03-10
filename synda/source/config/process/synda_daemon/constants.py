# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import signal
from daemon import DaemonContext
import daemon.pidfile

from synda.source.config.path.tree.default.models import Config as TreePath

from synda.source.config.file.internal.models import Config as Internal
from synda.source.config.file.daemon.models import Config as File

log_folder = TreePath().get("log")

pidfile = daemon.pidfile.PIDLockFile(
    File().default,
)

log_stdout = open(
    "{}/{}".format(
        log_folder,
        Internal().logger_consumer_file,
    ),
    "a+",
)
log_stderr = open(
    "{}/{}".format(
        log_folder,
        Internal().logger_consumer_file,
    ),
    "a+",
)
daemon_context = DaemonContext(
    working_directory=log_folder,
    pidfile=pidfile,
    stdout=log_stdout,
    stderr=log_stderr,
)


def terminate(signum, frame):
    # must be here because of double-fork (i.e. we can't move import at the top of this file,
    # because the first import must occur in 'main_loop' func).

    from synda.sdt import sdtaskscheduler
    sdtaskscheduler.terminate(signum, frame)


daemon_context.signal_map = {signal.SIGTERM: terminate, }
