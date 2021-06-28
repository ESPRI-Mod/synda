# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime
import numpy as np
import aiofiles
import asyncio

from synda.sdt import sdlog
from synda.source.process.asynchronous.download.worker.http.aio.task.models import Task as Base

from synda.source.config.file.user.preferences.models import Config as Preferences
preferences = Preferences()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    async def read_iter(self, response):
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        file_object = await aiofiles.open(local_path, mode='wb')
        async for chunk in response.aiter_bytes():
            response.raise_for_status()
            current_chunk_size = len(chunk)
            if not chunk:
                break
            file_size += current_chunk_size
            await file_object.write(chunk)

        return file_size

    # async def read_chunk(self, response):
    #     file_size = 0
    #     local_path = self.file_instance.get_full_local_path()
    #     async with aiofiles.open(local_path, mode='wb') as file_object:
    #         while True:
    #             chunk = await response.content.read(preferences.download_big_file_chunksize)
    #             current_chunk_size = len(chunk)
    #
    #             if not chunk:
    #                 break
    #
    #             file_size += current_chunk_size
    #             await file_object.write(chunk)
    #
    #     return file_size

    async def _download(self, client):
        begin = datetime.datetime.now()
        url = self.file_instance.url
        requestHeaders = {
            "Prefer": "respond-async",
        }
        # import httpx
        # timeout = httpx.Timeout(
        #     preferences.download_async_http_timeout / 2,
        #     # connect=preferences.download_async_http_timeout)
        #     connect=360,
        # )
        #
        # # http_client_session = httpx.AsyncClient(timeout=timeout)
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(url)
        # async with client.stream("GET", url, headers=requestHeaders) as response:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
        # async with client.get(url) as response:
            if preferences.download_big_file_chunksize is np.nan:
                file_size = await self.read_iter(response)
            else:
                raise Exception("httpx | big file task | read_chunk | not yet implemented")

                # file_size = await self.read_chunk(response)
            if response.status_code == 200:
                status = 0

        end = datetime.datetime.now()
        elapsed = end - begin

        debug = True
        if debug:
            result = {
                "file_id": self.file_instance.file_id,
                "status": status,
                "name": self.get_name(),
                "observed_size": file_size,
                "expected_size": self.file_instance.size,
                "duration": elapsed.total_seconds(),
                "start_date": begin.strftime(DATE_FORMAT),
                "end_date": end.strftime(DATE_FORMAT),
                "strategy": "asyncio httpx",
                "sdget_status": self.file_instance.sdget_status,
                "sdget_error_msg": self.file_instance.sdget_error_msg,
                "local_path": self.file_instance.local_path,
                "process_name": "big file task",
            }
            print(result)

        return status

    async def download(self, http_client_session):

        status = -1

        try:
            status = await self._download(http_client_session)
        except asyncio.exceptions.TimeoutError:
            msg = "The operation has exceeded the given deadline. " \
                  "In the sdt.conf file, you should increase the value of the following parameter : " \
                  "[download]async_http_timeout "
            self.file_instance.sdget_error_msg = msg
        except Exception as e:
            self.file_instance.sdget_error_msg = str(e)
            sdlog.info(
                "BgF-TASK-001",
                "ERROR OCCURED DURING DOWNLOADING ( BIG FILE TASK ) : {} ".format(
                    self.file_instance.sdget_error_msg
                ),
            )
        finally:
            self.file_instance.sdget_status = status
        return status
