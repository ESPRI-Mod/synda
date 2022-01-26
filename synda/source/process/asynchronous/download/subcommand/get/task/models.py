# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.download.subcommand.get.task.aiohttp.models import Task as Base
from synda.source.process.asynchronous.download.task.aiohttp.processes import Process as DownloadProcess


class Task(Base):

    def __init__(self, file_instance, name, process_cls=DownloadProcess, verbose=False):
        Base.__init__(self, file_instance, name, process_cls=process_cls, verbose=verbose)

