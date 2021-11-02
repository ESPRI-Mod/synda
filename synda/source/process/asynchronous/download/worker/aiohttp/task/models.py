# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime
import aiofiles
import aiohttp
import asyncio
import ssl
import uvloop

from synda.sdt import sdlog
from synda.source.process.asynchronous.download.task.models import Task as Base
from synda.source.config.file.internal.models import Config as Internal
from synda.source.config.file.certificate.x509.models import Config as SecurityFile


uvloop.install()
esgf_x509_proxy = SecurityFile().get_credentials()
internal = Internal()
DOWNLOADING_LOGGER_NAME = internal.logger_consumer

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    async def read_iter(self, response):
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        file_object = await aiofiles.open(local_path, mode='wb')

        async for chunk, end_of_data in response.content.iter_chunks():
            if not self.killed_by_worker:
                current_chunk_size = len(chunk)
                if end_of_data:
                    break
                file_size += current_chunk_size
                await file_object.write(chunk)
            else:
                break

        await file_object.close()
        return file_size

    async def read_chunk(self, response, streaming_chunk_size):
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        file_object = await aiofiles.open(local_path, mode='wb')

        while True:
            if not self.killed_by_worker:
                chunk = await response.content.read(streaming_chunk_size)
                current_chunk_size = len(chunk)

                if not chunk:
                    break

                file_size += current_chunk_size
                await file_object.write(chunk)
            else:
                break

        await file_object.close()
        return file_size

    async def _download(self, client, config):
        process_name = ""
        url = self.file_instance.url
        status = -1
        local_file_size = 0

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(esgf_x509_proxy, esgf_x509_proxy)

        try:
            async with client.get(url, ssl=ssl_context) as response:
                if response.status == 200:
                    if config["streaming_chunk_size"]:
                        local_file_size = await self.read_chunk(
                            response,
                            config["streaming_chunk_size"],
                        )
                        process_name = "Customized Streaming {}".format(config["streaming_chunk_size"])
                    else:
                        local_file_size = await self.read_iter(response)
                        process_name = "Free Streaming"
                else:
                    self.file_instance.sdget_error_msg = f"HTTP ERROR : {response.status}"
        except aiohttp.ClientConnectorCertificateError as e:
            self.file_instance.sdget_error_msg = str(e)
        if not self.file_instance.sdget_error_msg:
            status = 0

        return status, local_file_size, process_name

    async def download(self, client, config):
        begin = datetime.datetime.now()
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
            self.file_instance.sdget_error_msg = msg
        except Exception as e:
            self.file_instance.sdget_error_msg = str(e)
            sdlog.info(
                "BgF-TASK-001",
                "Unexpected error occured during download coroutine : {}".format(
                    self.file_instance.sdget_error_msg
                ),
                logger_name=DOWNLOADING_LOGGER_NAME,
            )
        finally:
            self.file_instance.sdget_status = status

        end = datetime.datetime.now()
        elapsed = end - begin

        if self.verbose:
            result = {
                "file_id": self.file_instance.file_id,
                "size": self.file_instance.size,
                "duration": elapsed.total_seconds(),
                "start_date": begin.strftime(DATE_FORMAT),
                "end_date": end.strftime(DATE_FORMAT),
                "strategy": "asyncio aiohttp",
                "status": status,
                "sdget_status": self.file_instance.sdget_status,
                "sdget_error_msg": self.file_instance.sdget_error_msg,
                "local_path": self.file_instance.local_path,
                "process_name": process_name,
            }
            print("{},".format(result))

        results = dict(
            status=status,
            local_file_size=local_file_size,
            # local_checksum=local_checksum,
        )
        return results
