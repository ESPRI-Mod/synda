# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import aiohttp

from synda.sdt import sdconfig
from synda.sdt import sdutils
from synda.sdt import sdlog
from synda.sdt import sdtypes
from synda.sdt import sdnexturl

from synda.source.config.process.download.constants import get_http_clients
from synda.source.config.process.download.constants import get_transfer_protocols

from synda.source.process.asynchronous.manager.batch.models import Manager as Base
from synda.source.process.asynchronous.download.task.grid_ftp.models import Task as GridFtpTask

from synda.source.process.asynchronous.download.task.http.small_file.models import Task as HttpSmallFileTask
from synda.source.process.asynchronous.download.task.http.big_file.models import Task as HttpBigFileTask

from synda.source.process.asynchronous.download.worker.models import Worker

from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.config.process.download.constants import TRANSFER

UN_CHUNKED_MAX_FILE_SIZE = 795795708

client_timeout = 600
timeout = aiohttp.ClientTimeout(total=client_timeout)

preferences = Preferences()


class Manager(Base):

    def __init__(self, scheduler, worker_cls=Worker, max_workers=1, name="", verbose=False):
        Base.__init__(self, scheduler, worker_cls=worker_cls, max_workers=max_workers, name=name, verbose=verbose)

        # initializations
        self.http_client_session = None

        # settings
        self.http_client_session = aiohttp.ClientSession(timeout=timeout)
        self.cpt = 0

    def get_http_client_session(self):
        return self.http_client_session

    async def clean(self):
        await self.http_client_session.close()

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

    async def get_scheduler_task(self):
        return await self.get_scheduler().get_task(self.name)

    def create_task(self, file_instance):
        test_mode = False
        if test_mode:
            if file_instance.url.startswith("http") and not self.cpt:
                file_instance.url = "gsiftp://esgf-dn1.ceda.ac.uk:2811//esg_dataroot/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc"
                self.cpt += 1
        new_task = None
        if file_instance:
            task_name = "{} , {}".format(
                self.name,
                file_instance.url,
            )

            transfer_protocol = sdutils.get_transfer_protocol(file_instance.url)

            if transfer_protocol == get_transfer_protocols()['http']:
                http_client = sdconfig.http_client
                if http_client == get_http_clients()["wget"]:
                    if file_instance.size <= UN_CHUNKED_MAX_FILE_SIZE:
                        new_task = HttpSmallFileTask(
                            file_instance,
                            task_name,
                            verbose=self.verbose,
                        )
                    else:
                        new_task = HttpBigFileTask(
                            file_instance,
                            task_name,
                            verbose=self.verbose,
                        )

            elif transfer_protocol == get_transfer_protocols()['gridftp']:
                new_task = GridFtpTask(file_instance, task_name, verbose=self.verbose)

        return new_task

    async def get_task(self):
        file_instance = await self.get_scheduler_task()
        return self.create_task(file_instance) if file_instance else None
