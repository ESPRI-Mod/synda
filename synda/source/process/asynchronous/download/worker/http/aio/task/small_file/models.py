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
import numpy as np

from synda.source.process.asynchronous.download.worker.http.aio.task.models import Task as Base
from synda.source.config.file.user.preferences.models import Config as Preferences


DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
preferences = Preferences()


class Task(Base):
    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    async def read_response(self, http_client_session):
        status = -1
        data = ""
        url = self.file_instance.url
        response = await http_client_session.get(url)

        try:
            data = await response.read()
        except Exception as e:
            self.file_instance.sdget_error_msg = str(e)
            # print("downloading_process | exception {}".format(self.file_instance.print()))
        finally:
            status = 0 if response.status == 200 else -1
            self.file_instance.sdget_status = status
            response.close()

        return status, data

    async def download(self, http_client_session):

        waiting_times = []
        writing_times = []
        file_size = 0

        local_path = self.file_instance.get_full_local_path()

        begin = begin_waiting = datetime.datetime.now()
        read_response_status, data = await self.read_response(http_client_session)
        end_waiting = datetime.datetime.now()
        waiting_times.append(
            (end_waiting - begin_waiting).total_seconds(),
        )
        file_size = len(data)
        async with aiofiles.open(local_path, mode='wb') as f:
            begin_writing = datetime.datetime.now()
            await f.write(data)
            end_writing = datetime.datetime.now()
            writing_times.append(
                (end_writing - begin_writing).total_seconds(),
            )

        status = "done" if read_response_status == 0 else "error"

        end = datetime.datetime.now()
        elapsed = end - begin

        result = {
            "file_id": self.file_instance.file_id,
            "name": self.get_name(),
            "observed_size": file_size,
            "expected_size": self.file_instance.size,
            "duration": elapsed.total_seconds(),
            "waiting_times": np.array(waiting_times).sum(),
            "writing_times": np.array(writing_times).sum(),
            "start_date": begin.strftime(DATE_FORMAT),
            "end_date": end.strftime(DATE_FORMAT),
            "strategy": "asyncio aiohttp",
            "sdget_status": self.file_instance.sdget_status,
            "sdget_error_msg": self.file_instance.sdget_error_msg,
            "local_path": self.file_instance.local_path,
            "process_name": "small file task",
        }

        if self.verbose:
            print(result)

        return status
