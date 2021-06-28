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

from synda.sdt import sdlog
from synda.sdt import sdtime
from synda.sdt import sdtools
from synda.sdt import sdfiledao

from synda.sdt import sdexception
from synda.sdt import sdlogon
from synda.sdt import sdconfig

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.user.credentials.models import Config as Credentials
from synda.source.config.process.download.constants import TRANSFER

from synda.source.process.asynchronous.task.models import Task as Base

from synda.source.process.asynchronous.download.cleaning.models import Process as CleaningProcess
from synda.source.process.asynchronous.download.control.models import Control as DownloadControl

preferences = Preferences()
credentials = Credentials()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

DOWNLOAD_ERROR_MSG = "Error occured during download."


async def renew_certificate():
    try:
        sdlogon.renew_certificate(
            credentials.openid,
            credentials.password,
            force_renew_certificate=False,
        )

    except Exception as e:
        sdlog.error(
            "SDDMDEFA-502",
            "Exception occured while retrieving certificate ({})".format(e),
        )

        raise


class Task(Base):
    """
    Abstract class
    """
    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, name, verbose=verbose)

        # initializations

        self.file_instance = None
        # self.timeout = 0
        self.post_process_control = None
        self.cleaning = None

        # settings
        self.file_instance = file_instance
        self.post_process_control = DownloadControl(file_instance)
        self.cleaning = CleaningProcess(file_instance)
        # self.timeout = preferences.download_async_http_timeout

    def get_file_instance(self):
        return self.file_instance

    def set_status(self, status):
        Base.set_status(self, status)
        # if status == "running":
        #     sdfiledao.update_file_before_download(self.file_instance)
            # self.file_instance.status = "running"

    def compute_metrics(self):
        # compute metrics
        self.file_instance.end_date = sdtime.now()
        self.file_instance.duration = sdtime.compute_duration(self.file_instance.start_date, self.file_instance.end_date)
        self.file_instance.rate = sdtools.compute_rate(self.file_instance.size, self.file_instance.duration)

    def create_local_path(self):
        target = os.path.dirname(self.file_instance.get_full_local_path())
        if not os.path.exists(target):
            os.makedirs(target)

    async def post_process(self):

        self.compute_metrics()

        await self.post_process_control.process()

        if self.error():

            # NOW WE ARE SURE THAT A PROBLEM OCCURED DURING DOWNLOAD
            self.cleaning.process()

        self.set_status("done")

    def error(self):
        return self.file_instance.status == "error"

    def print_metrics(self):
        sdlog.info(
            "TASKMETR-001",
            "{} | Task {} - Status : {}".format(
                datetime.datetime.now(),
                self.get_name(),
                self.status,
            ),
        )

    async def pre_process(self):

        await renew_certificate()

        self.set_status("running")
        sdfiledao.update_file_before_download(self.file_instance)
        self.create_local_path()

    async def download(self, http_client_session):
        """
        Abstract method
        Must be implemented into child classes
        :return: status
        """
        pass

    async def process(self, http_client_session):

        begin = datetime.datetime.now()

        await self.pre_process()

        sdlog.info("JFPDMDEF-001", "Will download url={}".format(self.file_instance.url, ))

        if sdconfig.fake_download:
            self.file_instance.status = TRANSFER["status"]['done']
            self.file_instance.error_msg = ""
            self.file_instance.sdget_error_msg = ""
        else:
            status = await self.download(http_client_session)
            self.file_instance.status = status

        await self.post_process()

    async def killed(self):

        # cancel the task
        self.set_status("cancelled")

        # remove downloaded file that was in progress
        self.cleaning.process()

        # update the file instance
        self.file_instance.status = TRANSFER["status"]['error']
        self.file_instance.priority -= 1
        self.file_instance.error_msg = "Download process has been killed"

        sdlog.error(
            "SDDMDEFA-190",
            "{} (file_id={},url={},local_path={})".format(
                self.file_instance.error_msg,
                self.file_instance.file_id,
                self.file_instance.url,
                self.file_instance.local_path,
            ),
        )

        # update the DB file table
        sdfiledao.update_file(self.file_instance, commit=True)

        # add specific message into the log
        # check for fatal error
        if self.file_instance.sdget_status == 4:
            sdlog.info(
                "SDDMDEFA-147",
                "Stopping daemon as sdget.download() returned fatal error.",
            )
            raise sdexception.FatalException()
