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
import asyncio

from synda.sdt import sdget

from synda.source.config.file.scripts.models import Config as Scripts

from synda.source.process.asynchronous.download.task.models import Task as Base

from synda.source.config.file.user.preferences.models import Config as Preferences

preferences = Preferences()


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    async def subprocess(
            self,
            debug=False,
            timeout=preferences.download_async_http_timeout,
            verbosity=0,
            buffered=True,
            hpss=preferences.is_download_hpss,
    ):

        stderr = stdout = ""
        status = -1

        data_download_script_gridftp = Scripts().get("sdgetg")

        args = sdget.prepare_args(
            self.file_instance.url,
            self.file_instance.get_full_local_path(),
            data_download_script_gridftp,
            debug,
            timeout,
            verbosity,
            hpss,
        )

        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        try:
            stdout, stderr = await process.communicate()
            status = process.returncode
            stderr = stderr.decode("utf-8")
        except OSError as e:
            status = -1
            stderr = str(e)
        finally:
            if stderr:
                stderr = stderr.strip('\n')
                while "\n" in stderr:
                    stderr = stderr.replace('\n', " ")
            self.file_instance.sdget_status = status
            self.file_instance.sdget_error_msg = stderr
        return status, stderr

    async def download(self):

        waiting_times = []
        writing_times = []
        file_size = 0

        local_path = self.file_instance.get_full_local_path()

        begin = datetime.datetime.now()

        sdget_gridftp_download_status, script_stderr = await self.subprocess()

        end = datetime.datetime.now()
        waiting_times.append(
            (end - begin).total_seconds(),
        )
        writing_times.append(
            (end - begin).total_seconds(),
        )

        status = "done" if sdget_gridftp_download_status == 0 else "error"

        end = datetime.datetime.now()
        elapsed = end - begin

        return status
