#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdworkerutils.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains worker related objects."""

import sdapp
import sdlog
import threading

class WorkerThread(threading.Thread):
    def __init__(self,instance,queue,service):
        threading.Thread.__init__(self)
        self._queue=queue       # the queue where to push the item once work is done to deferre database I/O
        self._instance=instance # the item being processed
        self._service=service   # the service used to process the item

    def run(self):
        try:
            self._service.run(self._instance)
            self._queue.put(self._instance) # add item in queue to handle database I/O in the main process
        except:
            sdlog.error("SYDUTILS-024","Thread didn't complete successfully")

            # debug
            #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))
            #traceback.print_exc(file=sys.stderr)

            self._service.exception_occurs=True

