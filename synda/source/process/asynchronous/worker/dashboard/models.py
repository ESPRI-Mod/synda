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
from synda.source.process.asynchronous.worker.dashboard.event.models import Event


class DashBoard(Container):
    def __init__(self, manager, identifier=""):
        Container.__init__(self, identifier=identifier)

        self.event = None
        self.nb_running = 0
        self.nb_done = 0
        self.nb_cancelled = 0

        self.manager = manager
        self.event = Event(self)
        self.update_metrics()

    def get_event(self):
        return self.event

    def get_manager(self):
        return self.manager

    def get_tasks(self):
        return self.get_data()

    def nb_tasks(self):
        return len(self.get_tasks())

    def cancel_running_tasks(self):
        tasks = self.get_tasks()
        for task in tasks:
            if task.running:
                task.set_status("cancelled")

    def add_task(self, task):
        self.add(task)

    def get_metrics(self):
        return self.nb_running, self.nb_cancelled, self.nb_done

    def update_metrics(self):
        self.nb_running = self.calculate_nb_running_tasks()
        self.nb_cancelled = self.calculate_nb_cancelled_tasks()
        self.nb_done = self.calculate_nb_done_tasks()

    def print_metrics(self):
        self.update_metrics()
        print(
            "Batch {} | Tasks | {} running, {} done, {} cancelled".format(
                self.get_identifier(),
                self.nb_running,
                self.nb_done,
                self.nb_cancelled,
            ),
        )
        # print(
        #     "{} | Batch {} | Tasks | {} running, {} done, {} cancelled".format(
        #         datetime.datetime.now(),
        #         self.get_identifier(),
        #         self.nb_running,
        #         self.nb_done,
        #         self.nb_cancelled,
        #     ),
        # )

    def calculate_nb_running_tasks(self):
        result = 0
        for task in self.get_tasks():
            if task.running():
                result += 1
        # print("{} tasks running | Batch {}".format(result, self.get_identifier()))
        return result

    def calculate_nb_done_tasks(self):
        result = 0
        for task in self.get_tasks():
            if task.done():
                result += 1
        # print("{} tasks done | Batch {}".format(result, self.get_identifier()))
        return result

    def calculate_nb_cancelled_tasks(self):
        result = 0
        for task in self.get_tasks():
            if task.cancelled():
                result += 1
        # print("{} tasks cancelled | Batch {}".format(result, self.get_identifier()))
        return result
