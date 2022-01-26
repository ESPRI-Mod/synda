# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import time
import datetime
import aiofiles
import aiohttp
import asyncio
import ssl
import uvloop

from synda.sdt import sdlog
from synda.sdt.sdget import gridftp_download

from synda.source.config.file.internal.models import Config as Internal
from synda.source.config.file.certificate.x509.models import Config as SecurityFile
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.scripts.models import Config as Scripts
from synda.source.config.path.tree.certificate.x509.models import Config as SecurityPath
from synda.source.config.path.tree.models import Config as TreePath


uvloop.install()
esgf_x509_proxy = SecurityFile().get_credentials()
internal = Internal()
DOWNLOADING_LOGGER_NAME = internal.logger_consumer

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Process(object):

    def __init__(self, task):
        self.task = task

    async def _download(self, client, config):
        begin = datetime.datetime.now()
        process_name = "script gridftp"
        url = self.task.file_instance.url
        status = -1
        local_file_size = 0

        preferences = Preferences()
        local_full_filename = self.task.file_instance.get_full_local_path()
        # status, killed, script_stderr = await asyncio.to_thread(
        #     gridftp_download,
        #     url,
        #     local_full_filename,
        #     debug=False,
        #     timeout=preferences.download_async_http_timeout,
        #     verbosity=self.task.verbose,
        #     buffered=True,
        #     hpss=preferences.is_download_hpss,
        # )

        status, killed, script_stderr = gridftp_download(
            url,
            local_full_filename,
            debug=False,
            timeout=preferences.download_async_http_timeout,
            verbosity=self.task.verbose,
            buffered=True,
            hpss=preferences.is_download_hpss,
        )

        local_file_size = os.path.getsize(local_full_filename)

        self.task.file_instance.sdget_status = status
        self.task.file_instance.sdget_error_msg = script_stderr

        end = datetime.datetime.now()
        if self.task.verbose:
            self.print_download_metrics(
                begin,
                end,
                local_file_size,
                status,
                process_name,
            )
        return status, local_file_size, process_name

    def print_download_metrics(self, begin, end, file_size, status, process_name):
        elapsed = end - begin
        result = {
            "file_id": self.task.file_instance.file_id,
            "size": file_size,
            "duration": elapsed.total_seconds(),
            "start_date": begin.strftime(DATE_FORMAT),
            "end_date": end.strftime(DATE_FORMAT),
            "strategy": "script gridftp",
            "status": status,
            "sdget_status": self.task.file_instance.sdget_status,
            "sdget_error_msg": self.task.file_instance.sdget_error_msg,
            "local_path": self.task.file_instance.local_path,
            "process_name": process_name,
            "url": self.task.file_instance.url,
        }
        print("\n{},".format(result))

    async def execute(self, client, config):
        process_name = "Unknown"
        status = -1
        local_checksum = ""
        local_file_size = 0
        try:
            status, local_file_size, process_name = await self._download(client, config)
        except asyncio.exceptions.TimeoutError:
            msg = "The operation has exceeded the given deadline. " \
                  "Perhaps : 1 / The data node is unavailable or " \
                  "2 / You should increase the value of the following parameter : " \
                  "[download]async_http_timeout in the sdt.conf file"
            self.task.file_instance.sdget_error_msg = msg
        except Exception as e:
            self.task.file_instance.sdget_error_msg = str(e)
            sdlog.info(
                "BgF-TASK-001",
                "Unexpected error occured during download coroutine : {}".format(
                    self.task.file_instance.sdget_error_msg
                ),
                logger_name=DOWNLOADING_LOGGER_NAME,
            )
        finally:
            self.task.file_instance.sdget_status = status

        results = dict(
            status=status,
            local_file_size=local_file_size,
            # local_checksum=local_checksum,
        )
        return results
