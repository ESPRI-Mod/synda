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
import wget
import asyncio

from synda.sdt import sdlog
from synda.source.process.asynchronous.download.worker.http.blocking.myrequests.task.models import Task as Base

from synda.source.config.file.user.preferences.models import Config as Preferences
preferences = Preferences()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    def read(self):
        socket = None
        status = 0
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        url = self.file_instance.url
        try:
            filename = wget.download(url, out=local_path, bar=None)
            file_size = os.path.getsize(self.file_instance.get_full_local_path())
        except Exception as e:
            self.file_instance.sdget_error_msg = str(e)
            status = -1

        return status, file_size

    async def _download(self):
        begin = datetime.datetime.now()

        status, file_size = await asyncio.to_thread(self.read)

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
                "strategy": "asyncio wget",
                "sdget_status": self.file_instance.sdget_status,
                "sdget_error_msg": self.file_instance.sdget_error_msg,
                "local_path": self.file_instance.local_path,
                "process_name": "big file task",
            }
            print(result)

        return status

    async def download(self, http_client_session=None):

        status = -1

        try:
            status = await self._download()
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
