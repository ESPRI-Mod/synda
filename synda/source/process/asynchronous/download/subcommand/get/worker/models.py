# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.download.worker.models import Worker as Base
from synda.source.process.asynchronous.download.subcommand.get.task.models import Task as FileTask


class Worker(Base):

    def __init__(self, name, queue, manager, aiohttp_task_cls=FileTask, gridftp_task_cls=FileTask):
        Base.__init__(
            self,
            name,
            queue,
            manager,
            aiohttp_task_cls=aiohttp_task_cls,
            gridftp_task_cls=gridftp_task_cls,
        )

    def get_tasks_progression(self, args):
        tasks_progression = []
        for task in self.dashboard.get_tasks():
            tasks_progression.append(
                task.get_progression(),
            )
        return tasks_progression
