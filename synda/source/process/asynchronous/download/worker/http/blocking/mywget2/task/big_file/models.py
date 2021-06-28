# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import time
import os
import datetime
import asyncio
import subprocess
import concurrent.futures

from synda.sdt import sdlog
from synda.sdt import sdget
from synda.sdt import sdutils

from synda.source.config.file.wget.exit_status.models import Reader as WgetExitStatusReader
# from synda.source.config.file.wget.exit_status.exceptions import InvalidExistStatus
# from synda.source.config.file.wget.exit_status.exceptions import UnknownStatusError

from synda.source.process.asynchronous.download.worker.http.blocking.mywget2.task.models import Task as Base
from synda.source.config.file.scripts.models import Config as Scripts
from synda.source.config.file.user.preferences.models import Config as Preferences
preferences = Preferences()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    def read_test(self):
        status = 0
        time.sleep(1)
        return status, self.file_instance.size

    def set_exit_status_message(self, return_code):
        message = "UNKNOWN WGET EXIT STATUS"
        try:
            message = WgetExitStatusReader().get_exit_status_message(return_code)
        except Exception as e:
            message = str(e)
        finally:
            self.file_instance.sdget_error_msg = message

    async def run_subprocess_shell(self):
        return_code = -1
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        url = self.file_instance.url
        data_download_script_http = Scripts().get("sdget")
        hpss = preferences.is_download_hpss
        timeout = preferences.download_async_http_timeout
        debug = False
        verbosity = False
        li = sdget.prepare_args(
            url,
            local_path,
            data_download_script_http,
            debug,
            timeout,
            verbosity,
            hpss,
        )

        sdget_error_msg = "run_subprocess_shell / Unknown error during downloading"

        try:
            proc = await asyncio.create_subprocess_shell(
                " ".join(li),
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            # proc = await asyncio.create_subprocess_exec(
            #     *li,
            #     stdin=None,
            #     stdout=None,
            #     stderr=None,
            # )

            stderr, junk = await proc.communicate()

            return_code = proc.returncode

            # stdout = stdout.decode()
            stderr = stderr.decode()

            # stderr = status
            sdget_error_msg = str(stderr)

        except Exception as e:
            return_code = -1
        finally:
            status = return_code
            self.file_instance.sdget_error_msg = sdget_error_msg
            # self.set_exit_status_message(return_code)

        return status, file_size

    def get_status_output(self, args, **kwargs):
        """
        Args:
            args (list): command + arguments

        Notes
            - handle exit status conversion and raise exception if child didn't complete normally
            - also note that with this func, stderr and stdout are retrieved separately
              (was not the case in 'commands' module)
            - also note that there is a 'getstatusoutput' func in subprocess
              maybe better to use it directly
              (more info https://docs.python.org/3.3/library/subprocess.html#legacy-shell-invocation-functions)
        """

        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
        # kwargs['universal_newlines']=False
        kwargs['text'] = True

        p = subprocess.Popen(args, **kwargs)

        stdout, stderr = p.communicate()

        return p.returncode, stdout, stderr

    def read(self):
        file_size = 0
        local_path = self.file_instance.get_full_local_path()
        url = self.file_instance.url
        data_download_script_http = Scripts().get("sdget")
        hpss = preferences.is_download_hpss
        timeout = preferences.download_async_http_timeout
        debug = False
        verbosity = False
        try:
            li = sdget.prepare_args(
                url,
                local_path,
                data_download_script_http,
                debug,
                timeout,
                verbosity,
                hpss,
            )
            status, stdout, stderr = sdutils.get_status_output(li, shell=False)
            # status, stdout, stderr = self.get_status_output(li, shell=False)
            # file_size = os.path.getsize(self.file_instance.get_full_local_path())
            self.file_instance.sdget_error_msg = str(stderr)

        except Exception as e:
            self.file_instance.sdget_error_msg = str(e)
            status = -1

        return status, file_size

    def mythread(self):
        import threading
        t = threading.Thread(target=self.read)
        t.start()

    async def _download(self, executor):
        status = -1
        file_size = 0
        begin = datetime.datetime.now()
        loop = asyncio.get_running_loop()
        # executor = concurrent.futures.ProcessPoolExecutor()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                status, file_size = await loop.run_in_executor(executor, self.read)
            except Exception as e:
                print("####################################")
                print(e)
        # status, file_size = await asyncio.to_thread(self.read)
        # status, file_size = await self.run_subprocess_shell()
        # r = await asyncio.gather(self.run_subprocess_shell())
        # status = r[0][0]
        # file_size = r[0][1]
        # Wait for the result:
        # status, file_size = future.result()

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
                "strategy": "asyncio wget (script)",
                "sdget_status": self.file_instance.sdget_status,
                "sdget_error_msg": self.file_instance.sdget_error_msg,
                "local_path": self.file_instance.local_path,
                "process_name": "big file task",
            }
            print("{},".format(result))

        return status

    async def download(self, executor=None):

        status = -1

        try:
            status = await self._download(executor)
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
