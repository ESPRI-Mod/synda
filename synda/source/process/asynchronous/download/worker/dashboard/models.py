# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime


from synda.source.process.asynchronous.worker.dashboard.models import DashBoard as Base
from synda.source.config.process.download.constants import TRANSFER
from synda.source.process.asynchronous.download.worker.dashboard.event.models import Event


class DashBoard(Base):
    def __init__(self, manager, identifier=""):
        Base.__init__(self, manager, identifier=identifier)
        self.event = Event(self)

    def print_downloads_metrics(self):
        nb_done = 0
        nb_error = 0
        nb_waiting = 0
        nb_running = 0

        for task in self.get_tasks():
            if task.get_file_instance().status == TRANSFER["status"]["waiting"]:
                nb_waiting += 1
            elif task.get_file_instance().status == TRANSFER["status"]["running"]:
                nb_running += 1
            elif task.get_file_instance().status == TRANSFER["status"]["error"]:
                nb_error += 1
            elif task.get_file_instance().status == TRANSFER["status"]["done"]:
                nb_done += 1
        print(
            "{} | Batch {} | Downloads | {} waiting, {} running, {} error, {} done".format(
                datetime.datetime.now(),
                self.get_identifier(),
                nb_waiting,
                nb_running,
                nb_error,
                nb_done,
            ),
        )

    def print_metrics(self):
        Base.print_metrics(self)
        self.print_downloads_metrics()
