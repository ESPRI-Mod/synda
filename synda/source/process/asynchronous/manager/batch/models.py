# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio

from synda.source.containers import Container
from synda.source.process.asynchronous.worker.models import Worker
from synda.source.process.asynchronous.task.models import Task


class Manager(Container):

    def __init__(self, scheduler, worker_cls=Worker, max_workers=1, name="", verbose=False):
        Container.__init__(self, identifier="workers")

        # initializations
        self.verbose = False
        self.name = ""
        self.max_workers = 0
        self.scheduler = None
        self.dashboard = None
        self.worker_cls = ""
        # settings
        self.verbose = verbose
        self.name = name
        self.max_workers = max_workers
        self.scheduler = scheduler
        self.worker_cls = worker_cls

        self.create_workers()

    def get_worker_cls(self):
        return self.worker_cls

    def get_dashboard(self):
        return self.dashboard

    async def get_task(self):
        new_task = None
        name = await self.get_scheduler().get_task(self.name)
        if name:
            new_task = Task(name, verbose=self.verbose)
        return new_task

    def get_name(self):
        return self.name

    def get_workers(self):
        return self.get_data()

    def create_workers(self):
        for i in range(self.max_workers):
            name = str(i)
            self.create_worker(name)
            # self.add_asyncio_task(asyncio_task)

    def get_scheduler(self):
        return self.scheduler

    def get_all_dashboard_tasks(self):
        all_tasks = []
        for worker in self.get_workers():
            all_tasks.extend(
                worker.get_dashboard().get_tasks(),
            )
        return all_tasks

    def get_metrics(self):
        nb_running_tasks = 0
        nb_cancelled_tasks = 0
        nb_done_tasks = 0

        for worker in self.get_workers():
            current_nb_running, current_nb_cancelled, current_nb_done = \
                worker.get_metrics()

            nb_running_tasks += current_nb_running
            nb_cancelled_tasks += current_nb_cancelled
            nb_done_tasks += current_nb_done

        return nb_running_tasks, nb_cancelled_tasks, nb_done_tasks

    def authorizes_new_task(self):
        authorized = False
        if self.scheduler.authorizes_new_task():
            if not self.all_workers_are_busy():
                authorized = True
        return authorized

    async def has_new_task(self, queue):
        success = False
        if queue.empty():
            if self.authorizes_new_task():
                new_task = await self.get_task()
                if new_task:
                    queue.put_nowait(new_task)
                    success = True
        else:
            success = True
        return success

    def cancel_running_tasks(self):
        for worker in self.get_workers():
            worker.cancel_running_tasks()

    def print_metrics(self):
        for worker in self.get_workers():
            worker.print_metrics()

    def get_max_workers(self):
        return self.max_workers

    def create_worker(self, name):
        self.add(
            self.get_worker_cls()(name, asyncio.Queue(), self),
        )

    async def put_new_task(self, queue):
        new_task = None
        if self.scheduler.authorizes_new_task():
            if not self.all_workers_are_busy():
                new_task = await self.get_task()
                if new_task:
                    queue.put_nowait(new_task)
        return new_task

    def all_workers_are_busy(self):
        nb_running_tasks, nb_cancelled_tasks, nb_done_tasks = self.get_metrics()
        return nb_running_tasks == self.max_workers
