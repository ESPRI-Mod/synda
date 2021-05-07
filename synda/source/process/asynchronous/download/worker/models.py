# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio

from synda.sdt import sdlog
from synda.source.config.file.internal.models import Config as Internal

from synda.source.process.asynchronous.worker.models import Worker as Base

from synda.source.process.asynchronous.download.worker.dashboard.models import DashBoard

from synda.source.config.file.user.preferences.models import Config as Preferences
internal = Internal()
preferences = Preferences()


def activate_tests_for_fallback_strategy(task):
    status = 'error'
    file_instance = task.get_file_instance()
    file_instance.status = status


class Worker(Base):

    def __init__(self, name, queue, manager):
        Base.__init__(self, name, queue, manager)
        self.dashboard = DashBoard(self, identifier=self.name)

    async def post_process_task(self, task):
        await Base.post_process_task(self, task)
        file_id = task.get_file_instance().file_id
        test_mode = False

        # for fallback_strategy tests
        if test_mode:
            activate_tests_for_fallback_strategy(task)

        if task.error():

            # A PROBLEM OCCURED DURING DOWNLOAD

            # => new strategy
            # the file instance is updated to allow a new download attempt with another url (if exists)
            fallback_strategy = True if preferences.is_download_http_fallback else False

            if fallback_strategy:
                new_task = self.manager.get_fallback_task(task.get_file_instance())
                while new_task:
                    new_task.set_worker(self)
                    self.pre_process_task(new_task)
                    # next url case => another url has been set
                    try:
                        await new_task.process()

                        # for fallback_strategy tests
                        if test_mode:
                            activate_tests_for_fallback_strategy(new_task)
                        new_task = \
                            self.manager.get_fallback_task(new_task.get_file_instance()) if new_task.error() else None
                    except asyncio.CancelledError:
                        await new_task.killed()

        # marked it as done
        # self.queue.task_done()
        if self.manager.verbose:
            self.log_history(file_id)

    def log_history(self, file_id):
        logger_name = internal.logger_consumer
        sdlog.info(
            "D/L-HIST-001",
            "file_id : {} | Download Attempts History".format(
                file_id,
            ),
            logger_name=logger_name,
        )
        for task in self.get_dashboard().get_tasks():
            file_instance = task.get_file_instance()
            if file_instance.file_id == file_id:
                sdlog.info(
                    "D/L-HIST-002",
                    str(file_instance),
                    logger_name=logger_name,
                )
