# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.sdt import sdlog
from synda.sdt import sdtypes
from synda.sdt import sdnexturl
from synda.sdt import sdfiledao

from synda.source.process.asynchronous.download.worker.models import Worker as Base
from synda.source.process.asynchronous.download.subcommand.download.task.aiohttp.models import Task as AiohttpTask
from synda.source.process.asynchronous.download.subcommand.download.task.gridftp.models import Task as GridftpTask

from synda.source.config.file.internal.models import Config as Internal

internal = Internal()
DOWNLOADING_LOGGER_NAME = internal.logger_consumer


class Worker(Base):

    def __init__(self, name, queue, manager, aiohttp_task_cls=AiohttpTask, gridftp_task_cls=GridftpTask):
        Base.__init__(
            self,
            name,
            queue,
            manager,
            aiohttp_task_cls=aiohttp_task_cls,
            gridftp_task_cls=gridftp_task_cls,
        )

    def set_fallback_task(self, file_instance):
        # Hack
        #
        # Notes
        #     - We need a log here so to have a trace of the original failed transfer
        # (i.e. in case the url-switch succeed, the error msg will be reset)
        #

        sdlog.info(
            "SDDMDEFA-088",
            "Transfer failed: try to use another url ({})".format(file_instance.url),
            logger_name=DOWNLOADING_LOGGER_NAME,
        )
        new_file = sdtypes.File()
        new_file.copy(file_instance)

        new_url_found = sdnexturl.run(new_file)

        if new_url_found:
            sdlog.info(
                "SDDMDEFA-108",
                "Transfer marked for retry (error_msg='{}',url={},file_id={}".format(
                    new_file.error_msg,
                    new_file.url,
                    new_file.file_id,
                ),
                logger_name=DOWNLOADING_LOGGER_NAME,
            )
            sdfiledao.update_file(new_file)

    async def post_process_task(self, task, client, config):
        await Base.post_process_task(self, task)
        file_id = task.get_file_instance().file_id

        if task.error():

            # A PROBLEM OCCURED DURING DOWNLOAD

            # => new strategy
            # the file instance is updated to allow a new download attempt with another url (if exists)
            fallback_strategy = True if config["is_download_http_fallback"] else False

            if fallback_strategy:
                self.set_fallback_task(task.get_file_instance())

        if self.verbose:
            self.log_history(file_id, config["logger_consumer"])

    def log_history(self, file_id, logger_name):
        tasks = self.get_dashboard().get_tasks()
        nb_tasks = len(tasks)
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
