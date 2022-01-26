# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import datetime
import uvloop
from synda.sdt import sdtime
from synda.sdt import sdtools

from synda.sdt import sdexception
from synda.sdt import sdconfig

from synda.source.config.file.user.credentials.models import Config as Credentials
from synda.source.config.process.download.constants import TRANSFER

from synda.source.process.asynchronous.task.models import Task as Base
from synda.source.process.asynchronous.download.cleaning.models import Process as CleaningProcess
from synda.source.config.file.internal.models import Config as Internal

internal = Internal()
DOWNLOADING_LOGGER_NAME = internal.logger_consumer

uvloop.install()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


async def renew_certificate():
    from synda.sdt import sdlog
    from synda.sdt import sdlogon
    try:
        credentials = Credentials()
        sdlogon.renew_certificate(
            credentials.openid,
            credentials.password,
            force_renew_certificate=False,
        )

    except Exception as e:
        sdlog.error(
            "SDDMDEFA-502",
            "Exception occured while retrieving certificate ({})".format(e),
            logger_name=DOWNLOADING_LOGGER_NAME,
        )

        raise


class Task(Base):
    """
    Abstract class
    """
    def __init__(self, file_instance, name, process_cls, control_cls, verbose=False):
        Base.__init__(self, name, process_cls, verbose=verbose)

        # initializations

        self.file_instance = None
        # self.timeout = 0
        self.post_process_control = None
        self.cleaning = None

        # settings
        self.file_instance = file_instance
        self.post_process_control = control_cls(file_instance)
        self.cleaning = CleaningProcess(file_instance)

    def get_file_instance(self):
        return self.file_instance

    def set_status(self, status):
        Base.set_status(self, status)

    def compute_metrics(self):
        # compute metrics
        self.file_instance.end_date = sdtime.now()
        self.file_instance.duration = sdtime.compute_duration(self.file_instance.start_date, self.file_instance.end_date)
        self.file_instance.rate = sdtools.compute_rate(self.file_instance.size, self.file_instance.duration)

    def create_local_path(self):
        target = os.path.dirname(self.file_instance.get_full_local_path())
        if not os.path.exists(target):
            os.makedirs(target)

    async def post_process(self, incorrect_checksum_action, local_file_size, do_controls, local_checksum=""):
        self.compute_metrics()
        if do_controls:
            await self.post_process_control.process(
                incorrect_checksum_action,
                local_file_size,
                local_checksum,
            )

        if self.error():

            # NOW WE ARE SURE THAT A PROBLEM OCCURED DURING DOWNLOAD
            self.cleaning.process()

        # asyncio task is now done
        self.set_status("done")

    def error(self):
        return self.file_instance.status == "error"

    def print_metrics(self):
        from synda.sdt import sdlog
        sdlog.info(
            "TASKMETR-001",
            "{} | Task {} - Status : {}".format(
                datetime.datetime.now(),
                self.get_name(),
                self.status,
            ),
            logger_name=DOWNLOADING_LOGGER_NAME,
        )

    async def pre_process(self):

        await renew_certificate()

        self.set_status("running")
        self.create_local_path()

    async def download(self, client, config):
        """
        Abstract method
        Must be implemented into child classes
        :return: status
        """
        return dict()

    async def execute(self, client, config):
        from synda.sdt import sdlog
        begin = datetime.datetime.now()

        await self.pre_process()

        sdlog.info(
            "JFPDMDEF-001",
            "Will download url={}".format(self.file_instance.url, ),
            logger_name=DOWNLOADING_LOGGER_NAME,
        )

        if sdconfig.fake_download:
            self.file_instance.status = TRANSFER["status"]['done']
            self.file_instance.error_msg = ""
            self.file_instance.sdget_error_msg = ""
        else:
            download_results = await self.process.execute(client, config)
            await self.post_process(
                config["incorrect_checksum_action"],
                download_results["local_file_size"],
                config["do_post_download_controls"],
            )

    async def killed(self):
        from synda.sdt import sdlog
        # remove downloaded file that was in progress
        self.cleaning.process()

        # update the file instance
        self.file_instance.status = TRANSFER["status"]['error']
        self.file_instance.priority -= 1
        if not self.file_instance.error_msg:
            self.file_instance.error_msg = "Download process has been killed"

        # cancel the task
        self.set_status("cancelled")

        sdlog.error(
            "SDDMDEFA-190",
            "{} (file_id={},url={},local_path={})".format(
                self.file_instance.error_msg,
                self.file_instance.file_id,
                self.file_instance.url,
                self.file_instance.local_path,
            ),
            logger_name=DOWNLOADING_LOGGER_NAME,
        )

        # add specific message into the log
        # check for fatal error
        if self.file_instance.sdget_status != 0:
            sdlog.info(
                "SDDMDEFA-147",
                self.file_instance.sdget_error_msg,
                logger_name=DOWNLOADING_LOGGER_NAME,
            )
            raise sdexception.FatalException()
