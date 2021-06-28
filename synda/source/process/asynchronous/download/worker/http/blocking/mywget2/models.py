# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import concurrent.futures

from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.process.asynchronous.download.worker.http.models import Worker as Base
from synda.source.process.asynchronous.download.worker.http.blocking.mywget2.task.big_file.models \
    import Task

preferences = Preferences()


class Worker(Base):

    def __init__(self, name, queue, manager):
        Base.__init__(self, name, queue, manager, Task, Task)

    async def process_all_tasks(self, start_delay):
        ascending = not self.get_tasks_counter()
        ascending = False
        # with concurrent.futures.ThreadPoolExecutor() as pool:
        #     while await self.manager.has_new_task(self.queue, ascending):
        #         await self.process_task(pool)
        #         self.increment_tasks_counter()
        #         ascending = not self.get_tasks_counter()
        while await self.manager.has_new_task(self.queue, ascending):
            await self.process_task(None)
            self.increment_tasks_counter()
            ascending = not self.get_tasks_counter()
            ascending = False
        print("All tasks processed | Queue id : {}".format(id(self.queue)))
        return "{} | All tasks processed".format(
            self.name,
        )
