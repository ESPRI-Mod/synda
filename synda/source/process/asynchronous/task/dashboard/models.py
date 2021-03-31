# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime
from synda.source.containers import Container
from synda.source.process.asynchronous.task.models import Task


class TasksDashBoard(Container):
    def __init__(self, batch_manager, tasks, identifier=""):
        Container.__init__(self, identifier=identifier)

        self.manager = None
        self.nb_pending = 0
        self.nb_running = 0
        self.nb_done = 0
        self.nb_cancelled = 0

        self.manager = batch_manager
        self.set_tasks(tasks)
        self.update()

    def nb_tasks(self):
        return len(self.get_data())

    def set_tasks(self, tasks):
        for i, item in enumerate(tasks):
            name = "( Batch {} - Item {})".format(
                self.get_identifier(),
                i,
            )
            new_task = Task(name, self.manager)
            self.add(new_task)

    def get_current_workload(self):
        return self.nb_pending, self.nb_running, self.nb_cancelled, self.nb_done

    def update(self):
        self.nb_pending = self.calculate_nb_pending_tasks()
        self.nb_running = self.calculate_nb_running_tasks()
        self.nb_cancelled = self.calculate_nb_cancelled_tasks()
        self.nb_done = self.calculate_nb_done_tasks()

    def print_report(self):
        self.update()
        print(
            "{} | Batch {} | Tasks | {} pending, {} running, {} done, {} cancelled".format(
                datetime.datetime.now(),
                self.get_identifier(),
                self.nb_pending,
                self.nb_running,
                self.nb_done,
                self.nb_cancelled,
            ),
        )

    async def get_pending_task(self):
        eod = False
        found = False
        i = 0
        tasks = self.get_data()
        nb_tasks = len(tasks)
        while not found and not eod:
            if tasks[i].pending():
                found = True
            else:
                i += 1
                eod = i >= nb_tasks
        if eod:
            task = None
        else:
            task = tasks[i]
            # print(
            #     "{} | Task | {}".format(
            #         datetime.datetime.now(),
            #         task.get_name(),
            #     ),
            # )
        return task

    def calculate_nb_pending_tasks(self):
        result = 0
        for task in self.get_data():
            if task.pending():
                result += 1
        return result

    def calculate_nb_running_tasks(self):
        result = 0
        for task in self.get_data():
            if task.running():
                result += 1
        # print("{} tasks running | Batch {}".format(result, self.get_identifier()))
        return result

    def calculate_nb_done_tasks(self):
        result = 0
        for task in self.get_data():
            if task.done():
                result += 1
        # print("{} tasks done | Batch {}".format(result, self.get_identifier()))
        return result

    def calculate_nb_cancelled_tasks(self):
        result = 0
        for task in self.get_data():
            if task.cancelled():
                result += 1
        # print("{} tasks cancelled | Batch {}".format(result, self.get_identifier()))
        return result

    def has_pending_tasks(self):
        return self.calculate_nb_pending_tasks() != 0