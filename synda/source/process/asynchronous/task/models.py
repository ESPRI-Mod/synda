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
import datetime

uvloop.install()


class Event(object):
    def __init__(self, worker):
        self.worker = None
        # settings
        self.worker = worker

    def new_task_status(self, task):
        self.worker.new_task_status(task)


async def default_post_process(task):
    task.set_status("done")
    success = True
    return success


class Task(object):
    def __init__(self, name, verbose=False):

        # initialization
        self.allowed_statuses = ["pending", "running", "cancelled", "done"]
        self.worker = None
        self.verbose = False
        self.event = None
        self.name = ""
        self.status = ""

        # settings
        self.verbose = verbose
        self.name = name
        self.status = "pending"

    def get_event(self):
        return self.event

    def set_worker(self, worker):
        self.event = Event(worker)
        self.worker = worker

    def get_worker(self):
        return self.worker

    async def post_process(self, **download_results):
        pass

    async def process(self, *args):
        self.set_status("running")
        await asyncio.sleep(10)
        success = await default_post_process(self)
        return success

    def get_name(self):
        return self.name

    def set_status(self, status):
        if status in self.allowed_statuses:
            self.status = status
            self.event.new_task_status(self)

    def print_metrics(self):
        print(
            "{} | Manager : {} | worker : {} | Task name : {} - status : {}".format(
                datetime.datetime.now(),
                self.worker.get_manager().get_name(),
                self.worker.get_name(),
                self.get_name(),
                self.status,
            ),
        )

    def get_metrics(self):
        return "Manager : {} | worker : {} | Task name : {} - status : {}".format(
            self.worker.get_manager().get_name(),
            self.worker.get_name(),
            self.get_name(),
            self.status,
        )

    def done(self):
        return self.status == "done"

    def cancelled(self):
        return self.status == "cancelled"

    def pending(self):
        return self.status == "pending"

    def running(self):
        return self.status == "running"

    @property
    def killed_by_worker(self):
        return self.get_worker().stopped

    async def killed(self):
        pass
