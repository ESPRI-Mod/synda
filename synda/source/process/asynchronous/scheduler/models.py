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
import signal
import functools
import tabulate

from synda.source.containers import Container
from synda.source.process.asynchronous.manager.batch.models import Manager as BatchManager
from synda.source.process.asynchronous.task.provider.models import Default as DefaultTaskProvider
from synda.source.process.asynchronous.scheduler.event.models import Event
from synda.source.process.asynchronous.scheduler.report.models import Report
from synda.source.process.asynchronous.worker.watchdog.models import Worker as WatchDog
tabulate.PRESERVE_WHITESPACE = True
uvloop.install()


class Scheduler(Container):
    def __init__(
            self,
            batch_manager_class=BatchManager,
            task_provider_class=None,
            nb_max_workers=3,
            nb_max_batch_workers=1,
            verbose=False,
            build_report=False,
            identifier="asynchronous tasks scheduler",
    ):
        Container.__init__(self, identifier=identifier)

        # initializations
        self.task_provider_class = None
        self.task_provider = None
        self.event = None
        self.manager_cls = ""
        self.nb_max_workers = 0
        self.nb_max_batch_workers = 0
        self.watchdog = None

        self.task_provider_class = task_provider_class
        self.nb_max_workers = nb_max_workers
        self.nb_max_batch_workers = nb_max_batch_workers
        self.report = None
        self.verbose = False
        self.stopped = False

        # settings
        self.watchdog = WatchDog(self)
        self.event = Event(self)
        self.manager_cls = batch_manager_class
        self.verbose = verbose
        if build_report:
            self.report = Report(self)
        self.set_task_provider()
        self.create_managers()

    def set_stopped(self):
        self.stopped = True

    def stop(self, signame, loop):
        print("Download stop in progress. Please wait. It may take quite a bit of time")
        self.set_stopped()

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

    def set_task_provider(self):
        self.task_provider = self.task_provider_class()

    def get_manager(self, name):
        manager = None
        for batch_manager in self.get_managers():
            if name == batch_manager.get_name():
                manager = batch_manager
                break
        return manager

    def get_manager_names(self):
        names = []
        for batch_manager in self.get_managers():
            names.append(batch_manager.get_name())
        return names

    async def add_managers(self, names):
        nb_new_managers = 0
        for name in names:
            create = False
            if name not in self.get_manager_names():
                create = True
            else:
                if self.verbose:
                    print(f"Update manager : {name}")
                self.update_manager(name)
            if create:
                self.create_manager(name)
                nb_new_managers += 1
                msg = f"Info | New tasks, taken into account by the new manager '{name}'"
                if self.verbose:
                    print(msg)
        if nb_new_managers:
            tasks = self.get_workers_coroutines()
            await asyncio.gather(*tasks)

    async def get_task(self, batch_name):
        task, new_batch_names = await self.task_provider.get_task(batch_name)
        if new_batch_names:
            await self.add_managers(new_batch_names)
        if not task:
            nb_busy_workers, nb_not_busy_workers = self.get_workers_activity()
            if not nb_busy_workers:
                self.set_stopped()
        return task

    def update_manager(self, name):
        manager = self.get_manager(name)
        manager.update_workers()

    def create_manager(self, name):
        batch_manager = \
            self.get_manager_cls()(self, max_workers=self.nb_max_batch_workers, name=name, verbose=self.verbose)
        self.add(batch_manager)

    def create_managers(self):
        manager_names = self.task_provider.get_db_batch_names()
        for name in manager_names:
            self.create_manager(name)

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

    def get_workers_coroutines(self, *args):
        workers_coroutines = []
        for manager in self.get_managers():
            if manager.get_status() == "pending":
                manager.set_status("running")
                workers = manager.get_workers()
                for worker in workers:
                    workers_coroutines.append(
                        worker.process_all_tasks(*args)
                    )

        return workers_coroutines

    def cancel_running_tasks(self):
        for manager in self.get_managers():
            manager.cancel_running_tasks()

    def get_watchdog_coroutine(self):
        return self.watchdog.process()


async def main(
        nb_max_workers=3,
        nb_max_batch_workers=1,
        task_provider_class=DefaultTaskProvider,
        verbose=False,
        build_report=False,
):

    _scheduler = Scheduler(
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        task_provider_class=task_provider_class,
        verbose=verbose,
        build_report=build_report,
    )

    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(_scheduler.stop, signame, loop))

    # Get processes that are going to process the whole available tasks.
    tasks = _scheduler.get_workers_coroutines()
    # Wait until all worker processes finished.

    results = await asyncio.gather(*tasks)
    _scheduler.get_event().all_task_done()
    if _scheduler.verbose:
        _scheduler.print_metrics()


async def scheduler(
        nb_max_workers=3,
        nb_max_batch_workers=1,
        task_provider_class=DefaultTaskProvider,
        verbose=True,
        build_report=False,
):
    await main(
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        task_provider_class=task_provider_class,
        verbose=verbose,
        build_report=build_report,
    )
