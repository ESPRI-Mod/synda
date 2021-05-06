# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime
import sys
import shutil
import os
import asyncio

from synda.source.process.asynchronous.worker.watchdog.event.models import Event


class Worker(object):

    def __init__(self, scheduler):

        # initializations
        self.name = ""
        self.scheduler = None
        self.event = None
        self.all_task_done = False

        # settings
        self.scheduler = scheduler
        self.event = Event(self)
        self.task = None

    def get_event(self):
        return self.event

    def set_all_task_done(self, value):
        self.all_task_done = value

    async def process(self, timer=2):
        begin = datetime.datetime.now()
        try:
            while not self.all_task_done:

                print("Synda downloading process in progress...")
                print()
                print("Process begins at {}".format(begin))
                print()

                all_tasks = self.scheduler.get_all_dashboard_tasks()
                nb_others = 0
                for task in all_tasks:
                    if task.done() or task.cancelled():
                        nb_others += 1
                        metrics = task.get_metrics()
                        print(metrics)
                nb_running = 0
                for task in all_tasks:
                    if task.running():
                        metrics = task.get_metrics()
                        nb_running += 1
                        print(metrics)

                if nb_others > 0 and nb_others == len(all_tasks):
                    self.set_all_task_done(True)
                    end = datetime.datetime.now()
                    print(
                        "Process ends at {}".format(begin),
                    )
                    print(
                        "Elapsed time : {}".format(
                            end - begin,
                        )
                    )
                    print()

                else:
                    print()
                    print("Use Control-C to stop the process")
                    print()
                    await asyncio.sleep(timer)
                    os.system('cls' if os.name == 'nt' else 'clear')

        except asyncio.CancelledError:
            pass
        finally:
            pass
