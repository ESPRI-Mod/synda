# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.sdt import sdfiledao

from synda.source.process.asynchronous.download.task.aiohttp.models import Task as Base
from synda.source.process.asynchronous.download.task.aiohttp.processes import Process as DownloadProcess
from synda.source.process.asynchronous.download.subcommand.download.task.control.models import Control as DownloadControl


class Task(Base):
    """
    Abstract class
    """
    def __init__(
            self,
            file_instance,
            name,
            verbose=False,
    ):
        Base.__init__(
            self,
            file_instance,
            name,
            DownloadProcess,
            control_cls=DownloadControl,
            verbose=verbose,
        )

    def set_status(self, status):
        Base.set_status(self, status)
        if status == "running":
            sdfiledao.update_file_before_download(self.file_instance)
        elif status == "cancelled":
            sdfiledao.update_file(self.file_instance, commit=True)
        elif status == "done":
            sdfiledao.update_file_after_download(self.file_instance)
