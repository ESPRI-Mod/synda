# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio

from synda.source.process.asynchronous.worker.dashboard.models import DashBoard


class Worker(object):

    def __init__(self, name, queue, manager):

        # initializations
        self.queue = asyncio.Queue()
        self.name = ""
        self.manager = None

        # settings
        self.queue = queue
        self.name = name
        self.manager = manager
        self.dashboard = DashBoard(self, identifier=self.name)

    def get_name(self):
        return self.name

    def new_task_status(self, task):
        self.dashboard.get_event().new_task_status(task)
        self.manager.get_scheduler().get_event().new_task_status(task)

    def get_manager(self):
        return self.manager

    def get_dashboard(self):
        return self.dashboard

    def get_metrics(self):
        return self.dashboard.get_metrics()

    def print_metrics(self):
        self.dashboard.print_metrics()

    def pre_process_task(self, task):
        # task.set_worker(self)
        self.dashboard.add_task(task)

    async def post_process_task(self, task):
        pass

    def cancel_running_tasks(self):
        self.dashboard.cancel_running_tasks()

    async def process_task(self):
        if self.queue.empty():
            # at the moment, tasks manager refuses to deliver a new task
            # probably reason :
            #      1 / the maximum pool of workers for the current batch has been reached,
            #      2 / the maximum pool of workers for all running batches has been reached
            # => worker has to wait , why not 1 second, before a new attempt
            print("{} worker is waiting".format(self.name))
            await asyncio.sleep(1)
        else:
            # get a task out of the queue
            task = await self.queue.get()
            # process it if it is pending
            if task.pending():
                try:
                    self.pre_process_task(task)
                    task.set_worker(self)
                    await task.process()
                    await self.post_process_task(task)

                except asyncio.CancelledError:
                    await task.killed()
                finally:
                    self.queue.task_done()

    async def process_all_tasks(self, start_delay):
        await asyncio.sleep(start_delay)
        while await self.manager.has_new_task(self.queue):
            await self.process_task()
        return "{} | All tasks processed".format(
            self.name,
        )
