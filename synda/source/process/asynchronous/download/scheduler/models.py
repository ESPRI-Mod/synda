# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime
import asyncio

from synda.sdt import sdlog

from synda.source.process.asynchronous.scheduler.models import Scheduler as Base
from synda.source.process.asynchronous.download.manager.batch.models import Manager as BatchManager

from synda.source.process.asynchronous.download.task.provider.models import Provider as TaskProvider

from synda.source.config.file.user.preferences.models import Config as Preferences
preferences = Preferences()


class Scheduler(Base):
    def __init__(
            self,
            batch_manager_class,
            nb_max_workers=3,
            nb_max_batch_workers=1,
            verbose=False,
            build_report=False,
    ):

        Base.__init__(
            self,
            batch_manager_class,
            nb_max_workers=nb_max_workers,
            nb_max_batch_workers=nb_max_batch_workers,
            verbose=verbose,
            build_report=build_report,
            identifier="asynchronous downloads scheduler",
        )

    def set_task_provider(self):
        self.task_provider = TaskProvider()

    async def clean(self):
        for manager in self.get_managers():
            await manager.clean()

    def print_workers_activity(self, task):
        if self.verbose:
            task.print_metrics()
            nb_busy_workers, nb_not_busy_workers = self.get_workers_activity()
            sdlog.info(
                "SCHEDULE-001",
                "{} | Scheduler metrics : {} free worker(s), {} busy".format(
                    datetime.datetime.now(),
                    nb_not_busy_workers,
                    nb_busy_workers,
                ),
            )


async def main(
        batch_manager_class,
        nb_max_workers=3,
        nb_max_batch_workers=1,
        verbose=False,
        build_report=False,
):

    scheduler = Scheduler(
        batch_manager_class,
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        build_report=build_report,
    )

    # Create three worker tasks to process the queue concurrently.
    tasks = scheduler.get_workers_coroutines()
    # Wait until all worker tasks are cancelled.
    # results = await asyncio.gather(*tasks, return_exceptions=True)
    if tasks:
        try:
            done, pending = await asyncio.wait(tasks)
            for task in done:
                task.cancel()
        except asyncio.CancelledError:
            scheduler.cancel_running_tasks()
        finally:
            scheduler.print_metrics()
            await scheduler.clean()


async def scheduler(verbose=False, build_report=False):
    nb_max_workers = preferences.download_max_parallel_download
    nb_max_batch_workers = preferences.download_max_parallel_download_per_datanode
    # nb_max_batch_workers = 1
    await main(
        BatchManager,
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        build_report=build_report,
    )
