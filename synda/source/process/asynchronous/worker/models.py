# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
import uvloop

from synda.source.process.asynchronous.worker.dashboard.models import DashBoard
from synda.source.process.asynchronous.task.models import Task
from synda.source.process.asynchronous.task.processes import Process

uvloop.install()


class Worker(object):

    def __init__(self, name, queue, manager):

        # initializations
        self.queue = asyncio.Queue()
        self.name = ""
        self.manager = None
        self.status = ""
        self.allowed_statuses = []

        # settings
        self.queue = queue
        self.name = name
        self.manager = manager
        self.dashboard = DashBoard(self, identifier=self.name)
        self.allowed_statuses = ["waiting", "running", "done"]

    @property
    def verbose(self):
        return self.get_manager().verbose

    def get_allowed_statuses(self):
        return self.allowed_statuses

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @property
    def stopped_by_manager(self):
        return self.get_manager().stopped_by_scheduler

    @property
    def stopped(self):
        return self.stopped_by_manager

    def new_task_status(self, task):
        self.dashboard.get_event().new_task_status(task)
        self.manager.get_scheduler().get_event().new_task_status(task)

    def get_manager(self):
        return self.manager

    def get_dashboard(self):
        return self.dashboard

    def get_messages(self):
        return self.dashboard.get_messages()

    def get_metrics(self):
        return self.dashboard.get_metrics()

    def print_metrics(self):
        if self.verbose:
            self.dashboard.print_metrics()

    def pre_process_task(self, task):
        # task.set_worker(self)
        self.dashboard.add_task(task)

    async def post_process_task(self, *args):
        pass

    def cancel_running_tasks(self):
        self.dashboard.cancel_running_tasks()

    def create_task(self, name):
        return Task(name, Process, verbose=self.verbose)

    async def process_task(self, *args):
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
            scheduler_task = await self.queue.get()
            task = self.create_task(scheduler_task)
            # process it if it is pending
            if task.pending():
                try:
                    self.pre_process_task(task)
                    task.set_worker(self)
                    await task.execute(*args)
                    await self.post_process_task(task)

                except asyncio.CancelledError:
                    await task.killed()
                finally:
                    self.queue.task_done()

    async def process_all_tasks(self, *args):
        while not self.stopped_by_manager:
            if not self.get_status() == "done":
                if self.manager.authorizes_new_task():
                    if await self.manager.has_new_task(self.queue):
                        await self.process_task(*args)
                    else:
                        self.set_status("done")
                else:
                    # at the moment, manager refuses to deliver a new task
                    # probably reason :
                    #      1 / the maximum pool of workers for the current batch has been reached,
                    #      2 / the maximum pool of workers for all running batches has been reached
                    # => worker has to wait , why not 1 second, before a new attempt
                    self.set_status("waiting")
                    print("{} worker is waiting".format(self.name))
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

        return "{} | All tasks processed".format(
            self.name,
        )
