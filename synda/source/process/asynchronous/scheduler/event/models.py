# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
class Event(object):

    def __init__(self, scheduler):
        self.scheduler = None
        self.scheduler = scheduler

    def all_task_done(self):
        self.scheduler.watchdog.get_event().all_task_done()

    def new_task_status(self, task):
        self.scheduler.print_workers_activity(task)
        if self.scheduler.get_report():
            self.scheduler.get_report().add_metrics()
