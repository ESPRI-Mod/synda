# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.manager.batch.models import Manager as Base
from synda.source.process.asynchronous.download.worker.models import Worker

from synda.source.config.file.user.preferences.models import Config as Preferences

preferences = Preferences()


class Manager(Base):

    def __init__(self, scheduler, worker_cls=Worker, max_workers=1, name="", verbose=False):
        Base.__init__(self, scheduler, worker_cls=worker_cls, max_workers=max_workers, name=name, verbose=verbose)

    async def has_new_task(self, queue, ascending):
        success = False
        if queue.empty():
            if self.authorizes_new_task():
                scheduler_task = await self.get_scheduler_task(ascending)
                if scheduler_task:
                    # print("New task (id : {}) added to queue with id : {}".format(scheduler_task.file_id, id(queue)))
                    queue.put_nowait(scheduler_task)
                    success = True
        else:
            success = True
        return success
