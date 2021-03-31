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
import tabulate
tabulate.PRESERVE_WHITESPACE = True

from synda.source.containers import Container
from synda.source.process.asynchronous.manager.batch.models import Manager as BatchManager


def get_batches():
    batches = [
        range(5),
        range(3),
        range(7),
    ]
    return batches


class Report(object):
    def __init__(self, manager):
        self.manager = None
        self.manager = manager


class Scheduler(Container):
    def __init__(self, nb_max_workers=3, nb_max_batch_workers=1, verbose=False, print_report=False):
        Container.__init__(self, identifier="asynchronous tasks manager")

        # initializations
        self.nb_max_workers = 0

        self.nb_max_workers = nb_max_workers
        self.nb_max_batch_workers = nb_max_batch_workers
        self.report = None
        self.verbose = False

        # settings
        self.verbose = verbose
        if print_report:
            self.report = Report(self)
        self.create_workers()
        self.print_current_report_if_required(first=True)

    def is_new_task_allowed(self):
        nb_pending_tasks, nb_busy_workers, nb_available_workers = self.get_current_metrics()
        return nb_pending_tasks > 0 and nb_available_workers > 0

    def get_current_workload(self):
        nb_pending_tasks = 0
        nb_running_tasks = 0
        nb_cancelled_tasks = 0
        nb_done_tasks = 0

        for batch_manager in self.get_data():
            current_nb_pending, current_nb_running, current_nb_cancelled, current_nb_done = \
                batch_manager.get_current_workload()

            nb_pending_tasks += current_nb_pending
            nb_running_tasks += current_nb_running
            nb_cancelled_tasks += current_nb_cancelled
            nb_done_tasks += current_nb_done

        return nb_pending_tasks, nb_running_tasks, nb_cancelled_tasks, nb_done_tasks

    def print_current_report_if_required(self, first=False):
        if self.report:
            report = [datetime.datetime.now().time()]
            headers = ["Time"]
            nb_workers = 0
            for batch_manager in self.get_data():
                current_nb_pending, current_nb_running, current_nb_cancelled, current_nb_done = \
                    batch_manager.get_current_workload()
                nb_workers += current_nb_running
                # if first:
                #     headers.extend(["batch", "running", "done"])
                headers.extend(["batch", "running", "done"])
                report.extend(
                    [
                        "{:12}".format(int(batch_manager.get_name())),
                        "{:12}".format(current_nb_running),
                        "{:12}".format(current_nb_done),
                    ],
                )

            headers.append("nb_workers")
            report.append("{:12}".format(nb_workers))

            # if first:
            #     print("TIME & TASKS STATUS CHANGE".center(160, " "))
            #     print()
            #     print(tabulate.tabulate([report], headers, colalign=("right",)))
            # else:
            #     print(tabulate.tabulate([report], colalign=("right",)))

            print(tabulate.tabulate([report], headers, colalign=("right",), tablefmt="html"))

    def get_current_metrics(self):
        nb_pending_tasks, nb_running_tasks, nb_cancelled_tasks, nb_done_tasks = self.get_current_workload()

        nb_busy_workers = nb_running_tasks
        nb_not_busy_workers = self.nb_max_workers - nb_busy_workers
        return nb_pending_tasks, nb_busy_workers, nb_not_busy_workers

    def print_verbose_if_required(self, task):
        if self.verbose:
            nb_pending_tasks, nb_busy_workers, nb_not_busy_workers = self.get_current_metrics()
            print(
                "{} | Current workload : {} free worker(s), {} busy".format(
                    datetime.datetime.now(),
                    nb_not_busy_workers,
                    nb_busy_workers,
                ),
            )
            task.print_verbose()

    def print_report_user_case_if_required(self, batches):
        if self.report:
            print("------------------------------------------")
            print("                USER CASE                 ")
            print()
            print(
                "  Maximum workers allowed : {}".format(
                    self.nb_max_workers,
                ),
            )
            report = []
            headers = ["Batch", "# Tasks", '# Maximum workers']
            for i, batch in enumerate(batches):
                report.append([i, len(batch), self.nb_max_batch_workers])
            print(tabulate.tabulate(report, headers, colalign=("right",), tablefmt="html"))
            print("------------------------------------------")
            print()

    def create_workers(self):
        batches = get_batches()
        self.print_report_user_case_if_required(batches)
        for i, batch in enumerate(batches):
            batch_manager = BatchManager(batch, self, max_workers=self.nb_max_batch_workers, name=str(i))
            self.add(batch_manager)

    def print_report(self):
        for batch_manager in self.get_data():
            batch_manager.print_report()

    def get_asyncio_tasks(self):
        tasks = []
        start_delay = 0
        step = 0
        for batch_manager in self.get_data():
            workers = batch_manager.get_workers()
            for worker in workers:
                tasks.append(
                    worker.process_task(start_delay)
                )
                start_delay += step

        return tasks


async def main(nb_max_workers=3, nb_max_batch_workers=1, verbose=False, print_report=False):

    scheduler = Scheduler(
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        print_report=print_report,
    )

    # Create three worker tasks to process the queue concurrently.
    tasks = scheduler.get_asyncio_tasks()
    # Wait until all worker tasks are cancelled.
    # results = await asyncio.gather(*tasks, return_exceptions=True)
    done, pending = await asyncio.wait(tasks)

    scheduler.print_report()
    for task in done:
        task.cancel()


async def scheduler(verbose=False, print_report=False):
    await main(nb_max_workers=6, nb_max_batch_workers=2, verbose=verbose, print_report=print_report)
