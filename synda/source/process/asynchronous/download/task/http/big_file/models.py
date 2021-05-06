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

from synda.source.process.asynchronous.download.task.http.models import Task as Base

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

optimized_chunk_sizes = 16384


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    async def read_chunk(self, response):
        return await response.content.read(optimized_chunk_sizes)

    async def download(self):

        begin = datetime.datetime.now()

        waiting_times = []
        writing_times = []
        downloading_chunk_lengths = []
        writing_chunk_lengths = []
        file_size = 0

        url = self.file_instance.url
        local_path = self.file_instance.get_full_local_path()

        try:
            async with self.get_client_session().get(url, allow_redirects=True) as response:
                async with aiofiles.open(local_path, mode='wb') as f:
                    while True:
                        # await asyncio.sleep(0.0005)
                        begin_waiting = datetime.datetime.now()
                        chunk = await self.read_chunk(response)
                        end_waiting = datetime.datetime.now()
                        waiting_times.append(
                            (end_waiting - begin_waiting).total_seconds(),
                        )
                        current_chunk_size = len(chunk)
                        downloading_chunk_lengths.append(current_chunk_size)

                        if not chunk:
                            break

                        current_writing_chunk_length = current_chunk_size
                        file_size += current_writing_chunk_length
                        writing_chunk_lengths.append(current_writing_chunk_length)
                        begin_writing = datetime.datetime.now()
                        await f.write(chunk)
                        end_writing = datetime.datetime.now()
                        writing_times.append(
                            (end_writing - begin_writing).total_seconds(),
                        )
                        current_chunk_sizes = downloading_chunk_lengths
        except Exception as e:
            self.file_instance.sdget_error_msg = str(e)
            print(
                "sdget_error_msg : {}".format(
                    self.file_instance.sdget_error_msg,
                ),
            )
        finally:
            status = 0 if response.status == 200 else -1
            self.file_instance.sdget_status = status

        end = datetime.datetime.now()
        elapsed = end - begin

        result = {
            "file_id": self.file_instance.file_id,
            "name": self.get_name(),
            "size": file_size,
            "duration": elapsed.total_seconds(),
            "waiting_times": np.array(waiting_times).sum(),
            "downloading_chunk_lengths": np.array(current_chunk_sizes).mean(),

            "writing_times": np.array(writing_times).sum(),
            "writing_chunk_lengths": np.array(downloading_chunk_lengths).mean(),

            "downloaded mean chunk size observed": np.array(writing_chunk_lengths).mean(),
            "start_date": begin.strftime(DATE_FORMAT),
            "end_date": end.strftime(DATE_FORMAT),
            "strategy": "asyncio aiohttp",
            "sdget_status": self.file_instance.sdget_status,
            "sdget_error_msg": self.file_instance.sdget_error_msg,
            "local_path": self.file_instance.local_path,
            "process_name": "small file task",
        }

        # if self.verbose:
        #     print(result)

        return status
