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
import uvloop
import signal
import functools


from synda.sdt import sdlog

from synda.source.process.asynchronous.scheduler.models import Scheduler as Base

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.internal.models import Config as Internal
from synda.sdt.sdfiledao import cleanup_running_transfer

EMPTY_QUEUE_MESSAGE = """
Download queue is empty.
Load the queue with the 'synda install' subcommand and try again : 'synda download start'.
"""
internal = Internal()
DOWNLOADING_LOGGER_NAME = internal.logger_consumer
preferences = Preferences()

uvloop.install()


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
            nb_max_workers=nb_max_workers,
            nb_max_batch_workers=nb_max_batch_workers,
            verbose=verbose,
            build_report=build_report,
            identifier="asynchronous downloads scheduler",
        )

        # initializations
        self.config = dict()

        # settings
        self.config = config

    def get_config(self):
        return self.config

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
                logger_name=DOWNLOADING_LOGGER_NAME,
            )

    def get_workers_coroutines(self, config=None):
        return Base.get_workers_coroutines(
            self,
            self.get_config(),
        )

    def stop(self, signame, loop):
        Base.stop(self, signame, loop)


async def main(
        batch_manager_class,
        task_provider,
        config,
        nb_max_workers=3,
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
    tasks = _scheduler.get_workers_coroutines()
    success = False
    if tasks:
        try:
            results = await asyncio.gather(*tasks)
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

            cleanup_running_transfer()

    else:
        print(EMPTY_QUEUE_MESSAGE)
    return success
