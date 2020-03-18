#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains worker related objects."""

import threading
from sdt.bin.commons.utils import sdlog, sdtrace
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdexception


class WorkerThread(threading.Thread):
    """This class is the thread that handle the file transfer."""

    def __init__(self, instance, queue, service):
        threading.Thread.__init__(self)
        self._queue = queue  # the queue where to push the item once work is done to deferre database I/O
        self._instance = instance  # the item being processed
        self._service = service  # the service used to process the item

    def run(self):
        try:
            self._service.run(self._instance)  # calls Download.run()
            self._queue.put(self._instance)  # add item in queue to handle database I/O in the main process
        except sdexception.CertificateRenewalException as e:
            # error occured during certificate renewal

            sdlog.error("SDWUTILS-003", "Certificate error: the daemon must be stopped")
            sdlog.error("SDWUTILS-001", "Thread didn't complete successfully")

            # no need to log stacktrace here as exception is already logged downstream
            # we always stop daemon in this case, as download can't succeed without a working certificate.
            # TODO: but sometimes, it's just a temporary failure (e.g. DNS failure during openid resolution),
            # so maybe wait for 5 or 6 transfers to fail in a row before stopping the daemon.

            self._service.exception_occurs = True

        except Exception as e:
            sdlog.error("SDWUTILS-002", "Thread didn't complete successfully")
            sdtrace.log_exception(stderr=True)

            if sdconfig.stop_download_if_error_occurs:
                self._service.exception_occurs = True
