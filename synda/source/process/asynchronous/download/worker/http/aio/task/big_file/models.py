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
        async for chunk, end_of_data in response.content.iter_chunks():
            current_chunk_size = len(chunk)
            if end_of_data:
                break
            file_size += current_chunk_size
            await file_object.write(chunk)

        return file_size

    async def read_chunk(self, response):
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        async with aiofiles.open(local_path, mode='wb') as file_object:
            while True:
                chunk = await response.content.read(preferences.download_big_file_chunksize)
                current_chunk_size = len(chunk)

                if not chunk:
                    break

                file_size += current_chunk_size
                await file_object.write(chunk)

        return file_size

    async def _download(self, http_client_session):
        begin = datetime.datetime.now()
        url = self.file_instance.url

        async with http_client_session.get(url, allow_redirects=True) as response:
            if preferences.download_big_file_chunksize is np.nan:
                file_size = await self.read_iter(response)
            else:
                file_size = await self.read_chunk(response)
            if response.status == 200:
                status = 0

        end = datetime.datetime.now()
        elapsed = end - begin

        debug = True
        if debug:
            result = {
                "file_id": self.file_instance.file_id,
                "name": self.get_name(),
                "observed_size": file_size,
                "expected_size": self.file_instance.size,
                "duration": elapsed.total_seconds(),
                "start_date": begin.strftime(DATE_FORMAT),
                "end_date": end.strftime(DATE_FORMAT),
                "strategy": "asyncio aiohttp",
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
