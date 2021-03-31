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
from tabulate import tabulate
# for generation of uml documentation
# from synda.source.process.asynchronous.manager.batch.models import Manager as BatchManager


async def default_post_process(task):
    task.set_status("done")
    success = True
    return success


class Task(object):
    def __init__(self, name, manager):

        # initialization
        self.manager = None
        # for generation of uml documentation
        # self.batch_manager = BatchManager([])
        self.name = ""
        self.status = ""

        # settings
        self.name = name
        self.manager = manager
        self.status = "pending"

    def update_tasks_dashboard(self):
        return self.manager.update_tasks_dashboard()

    def print_current_report_if_required(self):
        self.manager.get_scheduler().print_current_report_if_required()

    def print_verbose_if_required(self, task):
        return self.manager.get_scheduler().print_verbose_if_required(task)

    async def process(self):
        self.set_status("running")
        self.print_verbose_if_required(self)
        await asyncio.sleep(10)
        success = await default_post_process(self)
        return success

    def get_name(self):
        return self.name

    def set_status(self, status):
        self.status = status
        self.update_tasks_dashboard()
        self.print_current_report_if_required()

    def print_verbose(self):
        print(
            "{} | Task {} - Status : {}".format(
                datetime.datetime.now(),
                self.get_name(),
                self.status,
            ),
        )

    def done(self):
        return self.status == "done"

    def cancelled(self):
        return self.status == "cancelled"

    def pending(self):
        return self.status == "pending"

    def running(self):
        return self.status == "running"
