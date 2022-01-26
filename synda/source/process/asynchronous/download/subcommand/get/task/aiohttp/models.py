# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio

from synda.source.constants import bcolors
from synda.source.process.asynchronous.download.task.aiohttp.models import Task as Base
from synda.source.process.asynchronous.download.subcommand.get.task.control.models import Control as DownloadControl

SUCCESS_PREFIX = f'{bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC} File downloaded'
NO_CHECKSUM_SUCCESS_MESSAGE_TEMPLATE = SUCCESS_PREFIX + ', no checksum verification ({})'
VALIDATED_CHECKSUM_MESSAGE_TEMPLATE = SUCCESS_PREFIX + ', checksum OK ({})'

ERROR_PREFIX = f'{bcolors.FAIL + "ERROR" + bcolors.ENDC} Download Failed'
ERROR_MESSAGE_TEMPLATE = ERROR_PREFIX + " File {}, following error has been catched : {}"


class Task(Base):
    """
    Abstract class
    """
    def __init__(self, file_instance, name, control_cls=DownloadControl, process_cls=None, verbose=False):
        Base.__init__(self, file_instance, name, control_cls=control_cls, process_cls=process_cls, verbose=verbose)

    async def post_process(self, incorrect_checksum_action, local_file_size, do_controls, local_checksum=""):
        await Base.post_process(
            self,
            incorrect_checksum_action,
            local_file_size,
            do_controls,
            local_checksum=local_checksum,
        )
        # to be sure that all the subprocesses that depend on the task (for instance, the progression task displaying
        # used by the "get" subcommand) are done (before the task status "done" may stop the scheduler, and so these
        # subprocesses)

        await asyncio.sleep(1)
        if self.done():
            if not self.file_instance.error_msg and not self.file_instance.sdget_error_msg:
                if do_controls:
                    self.set_message(
                        VALIDATED_CHECKSUM_MESSAGE_TEMPLATE.format(
                            self.file_instance.local_path,
                        ),
                    )
                else:
                    self.set_message(
                        NO_CHECKSUM_SUCCESS_MESSAGE_TEMPLATE.format(
                            self.file_instance.local_path,
                        ),
                    )
            else:
                catched_errors = dict()
                if self.file_instance.error_msg:
                    catched_errors["error_msg"] = self.file_instance.error_msg
                if self.file_instance.sdget_error_msg:
                    catched_errors["sdget_error_msg"] = self.file_instance.sdget_error_msg

                self.set_message(
                    ERROR_MESSAGE_TEMPLATE.format(
                        self.file_instance.local_path,
                        catched_errors,
                    ),
                )
