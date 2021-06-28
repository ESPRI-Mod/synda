# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
import httpx

from synda.source.process.asynchronous.download.worker.http.models import Worker as Base
from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.process.asynchronous.download.worker.http.x.task.small_file.models import Task as HttpSmallFileTask
from synda.source.process.asynchronous.download.worker.http.x.task.big_file.models import Task as HttpBigFileTask

preferences = Preferences()


class Worker(Base):

    def __init__(self, name, queue, manager):

        Base.__init__(self, name, queue, manager, HttpSmallFileTask, HttpBigFileTask)

    async def process_all_tasks(self, start_delay):

        timeout = httpx.Timeout(
            preferences.download_async_http_timeout / 2,
            # connect=preferences.download_async_http_timeout)
            connect=620,
        )

        # client = httpx.AsyncClient(timeout=timeout)

        # ascending = not self.get_tasks_counter()
        # while await self.manager.has_new_task(self.queue, ascending):
        #     await self.process_task(None)
        #     # await self.process_task(client)
        #     self.increment_tasks_counter()
        #     ascending = not self.get_tasks_counter()

        async with httpx.AsyncClient(timeout=timeout) as client:
            ascending = not self.get_tasks_counter()
            while await self.manager.has_new_task(self.queue, ascending):
                await self.process_task(client)
                self.increment_tasks_counter()
                ascending = not self.get_tasks_counter()
            # await client.close()

        print("All tasks processed | Queue id : {}".format(id(self.queue)))
        return "{} | All tasks processed".format(
            self.name,
        )
