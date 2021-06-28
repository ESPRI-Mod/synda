# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import threading
import asyncio
import tabulate

from synda.source.containers import Container
from synda.source.process.asynchronous.manager.batch.models import Manager as BatchManager
from synda.source.process.asynchronous.task.provider.models import Provider as TaskProvider
from synda.source.process.asynchronous.scheduler.event.models import Event
from synda.source.process.asynchronous.scheduler.report.models import Report
from synda.source.process.asynchronous.worker.watchdog.models import Worker as WatchDog
tabulate.PRESERVE_WHITESPACE = True


class Scheduler(Container):
    def __init__(
            self,
            batch_manager_class=BatchManager,
            nb_max_workers=3,
            nb_max_batch_workers=1,
            verbose=False,
            build_report=False,
            identifier="asynchronous tasks scheduler",
    ):
        Container.__init__(self, identifier=identifier)

        # initializations
        self.task_provider = None
        self.event = None
        self.manager_cls = ""
        self.nb_max_workers = 0
        self.nb_max_batch_workers = 0
        self.watchdog = None

        self.nb_max_workers = nb_max_workers
        self.nb_max_batch_workers = nb_max_batch_workers
        self.report = None
        self.verbose = False

        # settings
        self.watchdog = WatchDog(self)
        self.event = Event(self)
        self.manager_cls = batch_manager_class
        self.verbose = verbose
        if build_report:
            self.report = Report(self)
        self.set_task_provider()
        self.create_managers()

    def get_report(self):
        return self.report

    def get_event(self):
        return self.event

    def get_manager_cls(self):
        return self.manager_cls

    def authorizes_new_task(self):
        nb_busy_workers, nb_available_workers = self.get_workers_activity()
        return nb_available_workers > 0

    def get_metrics(self):
        nb_running_tasks = 0
        nb_cancelled_tasks = 0
        nb_done_tasks = 0

        for manager in self.get_managers():
            current_nb_running, current_nb_cancelled, current_nb_done = \
                manager.get_metrics()

            nb_running_tasks += current_nb_running
            nb_cancelled_tasks += current_nb_cancelled
            nb_done_tasks += current_nb_done

        return nb_running_tasks, nb_cancelled_tasks, nb_done_tasks

    def get_managers(self):
        return self.get_data()

    def get_workers_activity(self):
        nb_running_tasks, nb_cancelled_tasks, nb_done_tasks = self.get_metrics()

        nb_busy_workers = nb_running_tasks
        nb_not_busy_workers = self.nb_max_workers - nb_busy_workers
        return nb_busy_workers, nb_not_busy_workers

    def print_workers_activity(self, task):
        if self.verbose:
            task.print_metrics()
            nb_busy_workers, nb_not_busy_workers = self.get_workers_activity()
            print(
                "Scheduler metrics : {} free worker(s), {} busy".format(
                    nb_not_busy_workers,
                    nb_busy_workers,
                )
            )
            # print(
            #     "{} | Scheduler metrics : {} free worker(s), {} busy".format(
            #         datetime.datetime.now(),
            #         nb_not_busy_workers,
            #         nb_busy_workers,
            #     )
            # )

    def set_task_provider(self):
        self.task_provider = TaskProvider()

    async def get_task(self, batch_name):
        return await self.task_provider.get_task(batch_name)

    def create_managers(self):
        manager_names = self.task_provider.get_batch_names()
        for name in manager_names:
            batch_manager = \
                self.get_manager_cls()(self, max_workers=self.nb_max_batch_workers, name=name, verbose=self.verbose)
            self.add(batch_manager)

    def print_metrics(self):
        for batch_manager in self.get_managers():
            batch_manager.print_metrics()

    def get_all_dashboard_tasks(self):
        all_tasks = []
        for batch_manager in self.get_managers():
            all_tasks.extend(
                batch_manager.get_all_dashboard_tasks(),
            )
        return all_tasks

    def get_workers_coroutines(self):
        workers_coroutines = []
        start_delay = 0
        step = 0
        for manager in self.get_managers():
            workers = manager.get_workers()
            for worker in workers:
                workers_coroutines.append(
                    worker.process_all_tasks(start_delay)
                    # worker.process_all_tasks
                )
                start_delay += step

        # workers_coroutines.append(
        #     self.watchdog.process(),
        # )
        return workers_coroutines

    def get_workers_coroutines2(self):
        workers_coroutines = []
        start_delay = 0
        step = 0
        for manager in self.get_managers():
            workers = manager.get_workers()
            for worker in workers:
                workers_coroutines.append(
                    # worker.process_all_tasks(start_delay)
                    worker.process_all_tasks
                )
                start_delay += step

        # workers_coroutines.append(
        #     self.watchdog.process(),
        # )
        return workers_coroutines

    def cancel_running_tasks(self):
        for manager in self.get_managers():
            manager.cancel_running_tasks()

    def get_watchdog_coroutine(self):
        return self.watchdog.process()


async def main(
        nb_max_workers=3,
        nb_max_batch_workers=1,
        verbose=False,
        build_report=False,
):

    _scheduler = Scheduler(
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        build_report=build_report,
    )

    # Get processes that are going to process the whole available tasks.
    workers_coroutines = _scheduler.get_workers_coroutines()
    # Wait until all worker processes finished.
    done, pending = await asyncio.wait(workers_coroutines)

    _scheduler.get_event().all_task_done()

    _scheduler.print_metrics()
    for task in done:
        task.cancel()


async def scheduler(verbose=True, build_report=False):
    await main(
        nb_max_workers=3,
        nb_max_batch_workers=1,
        verbose=verbose,
        build_report=build_report,
    )
