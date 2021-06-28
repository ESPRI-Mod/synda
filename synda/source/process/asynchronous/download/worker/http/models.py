# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio

from synda.sdt import sdutils

from synda.source.config.process.download.constants import get_transfer_protocol
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.process.asynchronous.download.worker.models import Worker as Base

preferences = Preferences()


class Worker(Base):

    def __init__(self, name, queue, manager, small_file_task_cls, big_file_task_cls):
        Base.__init__(self, name, queue, manager)

        # initializations
        self.small_file_task_cls = None
        self.big_file_task_cls = None

        # settings
        self.small_file_task_cls = small_file_task_cls
        self.big_file_task_cls = big_file_task_cls

    def create_task(self, file_instance):
        new_task = None
        if file_instance:
            task_name = "{} , {}".format(
                self.name,
                file_instance.url,
            )

            transfer_protocol = sdutils.get_transfer_protocol(file_instance.url)

            if transfer_protocol == get_transfer_protocol():
                if file_instance.size <= preferences.download_big_file_size:
                    new_task = self.small_file_task_cls(
                        file_instance,
                        task_name,
                        verbose=self.verbose,
                    )
                else:
                    new_task = self.big_file_task_cls(
                        file_instance,
                        task_name,
                        verbose=self.verbose,
                    )

        return new_task

    async def process_task(self, session):
        if self.queue.empty():
            # print("Empty queue with id : {}".format(id(self.queue)))
            # at the moment, tasks manager refuses to deliver a new task
            # probably reason :
            #      1 / the maximum pool of workers for the current batch has been reached,
            #      2 / the maximum pool of workers for all running batches has been reached
            # => worker has to wait , why not 1 second, before a new attempt
            print("{} worker is waiting".format(self.name))
            await asyncio.sleep(0.1)
        else:
            # get a task out of the queue
            scheduler_task = await self.queue.get()
            # print("Task (id : {} / status : {}) for queue with id : {}".format(scheduler_task.file_id, scheduler_task.status, id(self.queue)))

            task = self.create_task(scheduler_task)
            # process it if it is pending
            if task.pending():
                try:
                    self.pre_process_task(task)
                    task.set_worker(self)
                    await task.process(session)
                    await self.post_process_task(task)

                except asyncio.CancelledError:
                    await task.killed()
                finally:
                    self.queue.task_done()

    async def process_all_tasks(self, start_delay):

        async with self.get_http_client_session() as client:
            ascending = not self.get_tasks_counter()
            while await self.manager.has_new_task(self.queue, ascending):
                await self.process_task(client)
                self.increment_tasks_counter()
                ascending = not self.get_tasks_counter()
            await client.close()

        print("All tasks processed | Queue id : {}".format(id(self.queue)))
        return "{} | All tasks processed".format(
            self.name,
        )
