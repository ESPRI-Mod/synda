# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
#################################
import sys
import time
import asyncio
import uvloop
import signal
import functools
import humanize
from tabulate import tabulate

from synda.source.process.asynchronous.download.scheduler.models import Scheduler as Base

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.internal.models import Config as Internal

from synda.source.process.asynchronous.download.subcommand.get.manager.models \
    import Manager as AiohttpBatchManager

EMPTY_QUEUE_MESSAGE = """
'No current download'
"""
internal = Internal()
DOWNLOADING_LOGGER_NAME = internal.logger_consumer
preferences = Preferences()

uvloop.install()


def display_several_downloads_report(tasks_progression):
    li = []
    nb_tasks_done = 0
    for task_progression in tasks_progression:
        if task_progression["current_size"] > 0:
            # Display only running downlads (excluding waiting ones)
            # Find the status of the checks
            if task_progression["current_size"] < task_progression["expected_size"]:
                # waiting status
                checks_status = ""
            elif task_progression["current_size"] == task_progression["expected_size"]:
                nb_tasks_done += 1
                checks_status = task_progression["status"] if task_progression["status"] == "running" else ""
            else:
                checks_status = "error"

            li.append(
                [
                    humanize.naturalsize(task_progression["current_size"], gnu=False),
                    humanize.naturalsize(task_progression["expected_size"], gnu=False),
                    task_progression["start_date"],
                    checks_status,
                    task_progression["data_node"],
                    task_progression["filename"],
                ],
            )

    if len(li) > 0:
        print(
            tabulate(
                li,
                headers=['Current size', 'Total size', 'Download start date', 'Checks', 'Data node',
                         'Filename'],
                tablefmt="plain",
            ),
        )

    return nb_tasks_done


def display_one_download_report(task_progression):
    if task_progression["current_size"] > 0:
        nb_chars = 50
        nb_equals = int(nb_chars * task_progression["current_size"] / task_progression["expected_size"])
        spaces = ' ' * (nb_chars - nb_equals)
        line = spaces.rjust(nb_chars, "=")
        # line = task_progression + "\n"
        sys.stdout.write(
            "\r{} [{}] {} KiB/s ({} / {})".format(
                task_progression["filename"],
                line,
                task_progression["rate"],
                humanize.naturalsize(
                    task_progression["current_size"],
                    gnu=False,
                ),
                humanize.naturalsize(
                    task_progression["expected_size"],
                    gnu=False,
                ),
            )
        )
        sys.stdout.flush()


class Scheduler(Base):
    def __init__(
            self,
            batch_manager_class,
            task_provider,
            config,
            nb_max_workers=3,
            nb_max_batch_workers=1,
            verbose=False,
            build_report=False,
    ):
        Base.__init__(
            self,
            batch_manager_class,
            task_provider,
            config,
            nb_max_workers=nb_max_workers,
            nb_max_batch_workers=nb_max_batch_workers,
            verbose=verbose,
            build_report=build_report,
        )

    def get_workers_tasks_progression(self, *args):
        tasks_progression = []
        for manager in self.get_managers():
            workers = manager.get_workers()
            for worker in workers:
                tasks_progression.extend(
                    worker.get_tasks_progression(*args),
                )

        return tasks_progression

    def _progress_task(self):

        # CURSOR_UP_ONE = '\x1b[1A'
        # ERASE_LINE = '\x1b[2K'

        nb_tasks = self.task_provider.get_nb_tasks()
        # Waiting time after all tasks have been done
        max_waiting_time = 2
        max_waiting_time_reached = False
        delay = internal.subcommand_get_display_downloads_progression_every_n_seconds
        current_waiting_time = 0
        nb_tasks_done = 0
        while not self.stopped and not nb_tasks_done == nb_tasks:
            tasks_progression = self.get_workers_tasks_progression(dict())
            nb_tasks_done = display_several_downloads_report(tasks_progression)
            # if nb_tasks == 1:
            #     if len(tasks_progression) == 1:
            #         task_progression = tasks_progression[0]
            #         display_one_download_report(task_progression)
            # elif nb_tasks > 1:
            #     display_several_downloads_report(tasks_progression)

            time.sleep(delay)

        # Last display to be sure to display
        tasks_progression = self.get_workers_tasks_progression(dict())
        display_several_downloads_report(tasks_progression)

        return "_progress_task_successfully_finished"

    async def progress_task(self):
        return await asyncio.to_thread(
            self._progress_task,
        )

async def main(
        batch_manager_class,
        task_provider,
        config,
        nb_max_workers=1,
        nb_max_batch_workers=1,
        verbose=False,
        build_report=False,
):

    _scheduler = Scheduler(
        batch_manager_class,
        task_provider,
        config,
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        build_report=build_report,
    )

    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(_scheduler.stop, signame, loop))

    # Create three worker tasks to process the queue concurrently.
    _scheduler.print_metrics()
    tasks = [_scheduler.progress_task()] if _scheduler.get_config()["verbosity"] else []
    tasks.extend(
        _scheduler.get_workers_coroutines(),
    )
    success = False
    if tasks:
        try:
            results = await asyncio.gather(*tasks)
            _scheduler.print_messages()
            if verbose:
                for result in results:
                    print(result)
            success = True
        except asyncio.CancelledError:
            _scheduler.cancel_running_tasks()
        except Exception as e:
            print(e)
            pass
        finally:
            if _scheduler.verbose:
                _scheduler.print_metrics()

    else:
        print(EMPTY_QUEUE_MESSAGE)
    return success


async def scheduler(
        task_provider,
        batch_manager=AiohttpBatchManager,
        nb_max_workers=preferences.download_max_parallel_download,
        nb_max_batch_workers=preferences.download_max_parallel_download_per_datanode,
        config=None,
        verbose=False,
        build_report=False,
):

    # nb_max_batch_workers = 1

    _config = dict(
            http_timeout=preferences.download_direct_http_timeout,
            streaming_chunk_size=preferences.download_streaming_chunk_size,
            incorrect_checksum_action=preferences.behaviour_incorrect_checksum_action,
            is_download_http_fallback=False,
            logger_consumer=internal.logger_consumer,
        )
    if not config:
        config = _config
    else:
        config.update(_config)

    success = await main(
        batch_manager,
        task_provider,
        config,
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        build_report=build_report,
    )

    return success
