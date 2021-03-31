# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
import datetime

from synda.source.process.asynchronous.worker.models import Worker
from synda.source.process.asynchronous.task.dashboard.models import TasksDashBoard


class Manager(object):

    def __init__(self, tasks, scheduler, max_workers=1, name=""):

        # initializations
        self.name = ""
        self.max_workers = 0
        self.workers = []
        self.scheduler = None
        self.tasks_dashboard = None
        # self.asyncio_tasks = []

        # settings
        self.name = name
        self.max_workers = max_workers
        self.workers = Worker(name, asyncio.Queue(), self)
        self.workers = []
        self.scheduler = scheduler
        self.tasks_dashboard = TasksDashBoard(self, tasks, identifier=name)

        self.create_workers()

    def get_name(self):
        return self.name

    def get_workers(self):
        return self.workers

    # def get_asyncio_tasks(self):
    #     return self.asyncio_tasks
    #
    # def add_asyncio_task(self, asyncio_task):
    #     self.asyncio_tasks.append(asyncio_task)

    def create_workers(self):
        for i in range(self.max_workers):
            name = "Batch {} | Worker {}".format(
                self.name,
                i,
            )
            self.create_worker(name)
            # self.add_asyncio_task(asyncio_task)

    def get_scheduler(self):
        return self.scheduler

    def get_current_workload(self):
        return self.tasks_dashboard.get_current_workload()

    def has_pending_tasks(self):
        nb_pending_tasks, nb_running_tasks, nb_cancelled_tasks, nb_done_tasks = self.get_current_workload()
        return nb_pending_tasks

    def update_tasks_dashboard(self):
        return self.tasks_dashboard.update()

    def print_report(self):
        self.tasks_dashboard.print_report()

    def get_max_workers(self):
        return self.max_workers

    def create_worker(self, name):
        # print(
        #     "{} | Newly created worker {}".format(
        #         datetime.datetime.now(),
        #         name,
        #     ),
        # )
        self.workers.append(
            Worker(name, asyncio.Queue(), self),
        )
        # return asyncio.create_task(
        #     self.workers[-1].process_task(start_delay),
        # )

    async def put_new_task(self, queue):
        pending_task = None
        if self.scheduler.is_new_task_allowed():
            if self.have_some_workers_not_busy():
                pending_task = await self.tasks_dashboard.get_pending_task()
                if pending_task:
                    queue.put_nowait(pending_task)
        return pending_task

    def have_some_workers_not_busy(self):
        self.tasks_dashboard.update()
        return self.tasks_dashboard.nb_running < self.max_workers
