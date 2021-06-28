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
from synda.sdt import sdtypes
from synda.sdt import sdnexturl

from synda.source.process.asynchronous.worker.models import Worker as Base
from synda.source.process.asynchronous.download.worker.dashboard.models import DashBoard

from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.file.internal.models import Config as Internal
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
        # initializations
        self.tasks_counter = 0
        # self.conn = None
        # settings
        self.dashboard = DashBoard(self, identifier=self.name)

    def increment_tasks_counter(self):
        self.tasks_counter += 1

    def get_tasks_counter(self):
        return self.tasks_counter

    def get_fallback_task(self, file_instance):
        # Hack
        #
        # Notes
        #     - We need a log here so to have a trace of the original failed transfer
        # (i.e. in case the url-switch succeed, the error msg will be reset)
        #

        sdlog.info(
            "SDDMDEFA-088",
            "Transfer failed: try to use another url ({})".format(file_instance.url),
        )
        new_file = sdtypes.File()
        new_file.copy(file_instance)

        new_url_found = sdnexturl.run(new_file)

        if new_url_found:
            new_file.status = TRANSFER["status"]['waiting']
            new_file.error_msg = None
            new_file.sdget_status = None
            new_file.sdget_error_msg = None
            new_file.start_date = None
            new_file.end_date = None
            sdlog.info(
                "SDDMDEFA-108",
                "Transfer marked for retry (error_msg='{}',url={},file_id={}".format(
                    new_file.error_msg,
                    new_file.url,
                    new_file.file_id,
                ),
            )
        return self.create_task(new_file) if new_url_found else None

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
                new_task = self.get_fallback_task(task.get_file_instance())
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
                            self.get_fallback_task(new_task.get_file_instance()) if new_task.error() else None
                    except asyncio.CancelledError:
                        await new_task.killed()

        if self.verbose:
            self.log_history(file_id)

    def log_history(self, file_id):
        tasks = self.get_dashboard().get_tasks()
        nb_tasks = len(tasks)
        logger_name = internal.logger_consumer
        sdlog.info(
            "D/L-HIST-001",
            "file id : {} | Downloads History".format(
                file_id,
            ),
            logger_name=logger_name,
        )
        nb_attempts = 0
        for task in tasks:
            file_instance = task.get_file_instance()
            if file_instance.file_id == file_id:
                nb_attempts += 1
                sdlog.info(
                    "D/L-HIST-002",
                    "file id : {} | Attempt # {}, file instance : {}".format(
                        file_id,
                        nb_attempts,
                        str(file_instance),
                    ),
                    logger_name=logger_name,
                )
