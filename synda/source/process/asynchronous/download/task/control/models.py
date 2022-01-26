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
import uvloop

from synda.sdt import sdutils
from synda.sdt.sdexception import FatalException

from synda.source.config.file.constants import CHECKSUM
from synda.source.config.process.download.constants import TRANSFER

uvloop.install()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

FILE_CORRUPTION_CHECKSUM_ERROR_MSG = "File corruption detected: local checksum doesn't match remote checksum"


class Control(object):

    def __init__(self, file_instance):

        # initializations
        self.file_instance = None

        # settings
        self.file_instance = file_instance

    def validate_file_size(self, local_file_size):
        validated = True
        error_msg = ""
        error_code = ""
        if hasattr(self.file_instance, "size"):

            if self.file_instance.size is not None:
                if int(self.file_instance.size) != local_file_size:
                    validated = False
                    error_code = "SDDMDEFA-002"
            else:
                validated = False
        else:
            validated = False

        return validated, error_code

    def validate_checksum(self, incorrect_checksum_action):
        validated = True
        error_code = ""
        local_checksum = ""

        if hasattr(self.file_instance, "checksum") and hasattr(self.file_instance, "checksum_type"):
            if self.file_instance.checksum:
                # retrieve remote checksum
                remote_checksum = self.file_instance.checksum

                if remote_checksum:
                    # remote checksum exists
                    begin = datetime.datetime.now()

                    checksum_type = self.file_instance.checksum_type \
                        if self.file_instance.checksum_type is not None else CHECKSUM['type']["md5"]

                    local_checksum = sdutils.compute_checksum(self.file_instance.get_full_local_path(), checksum_type)

                    end = datetime.datetime.now()
                    # compare local and remote checksum
                    if remote_checksum == local_checksum:
                        # checksum is ok
                        self.file_instance.status = TRANSFER["status"]['done']
                        self.file_instance.error_msg = ""
                    else:
                        # checksum is not ok
                        validated = False
                        if incorrect_checksum_action == "remove":
                            error_code = "SDDMDEFA-155"

                            self.file_instance.status = TRANSFER["status"]['error']
                            self.file_instance.priority -= 1
                            self.file_instance.error_msg = FILE_CORRUPTION_CHECKSUM_ERROR_MSG

                        elif incorrect_checksum_action == "keep":
                            error_code = "SDDMDEFA-157"

                            self.file_instance.status = TRANSFER["status"]['done']
                            self.file_instance.error_msg = ""
                        else:
                            raise FatalException(
                                "SDDMDEFA-507",
                                "incorrect value ({})".format(incorrect_checksum_action),
                            )
                else:
                    error_msg = ""
                    # remote checksum is missing
                    # NOTE: we DON'T store the local checksum ('file' table contains only the *remote* checksum)

                    self.file_instance.status = TRANSFER["status"]['done']
                    self.file_instance.error_msg = error_msg
            else:
                validated = False
        else:
            error_code = "SDDMDEFA-160"
            validated = False

        return validated, error_code, local_checksum

    def _process(self, incorrect_checksum_action, local_file_size):
        # 1 / file size must be the expected one
        validated = self.validate_file_size(local_file_size)
        if validated:
            # 1 / checksum must be correct
            validated = self.validate_checksum(incorrect_checksum_action)
        return validated

    async def process(self, incorrect_checksum_action, local_file_size, local_checksum):
        validated = False
        begin = datetime.datetime.now()
        may_be_a_success = \
            os.path.exists(
                self.file_instance.get_full_local_path(),
            ) and (self.file_instance.sdget_status == 0 or self.file_instance.sdget_status is None)
        if may_be_a_success:
            # MORE CONTROLS ARE REQUIRED TO BE SURE THAT NO PROBLEM OCCURED DURING DOWNLOAD
            validated = await asyncio.to_thread(
                self._process,
                incorrect_checksum_action,
                local_file_size,
            )
        else:
            self.file_instance.status = TRANSFER["status"]['error']

        end = datetime.datetime.now()
        elapsed = end - begin

        debug = False
        if debug:
            result = {
                "file_id": self.file_instance.file_id,
                "size": self.file_instance.size,
                "duration": elapsed.total_seconds(),
                "start_date": begin.strftime(DATE_FORMAT),
                "end_date": end.strftime(DATE_FORMAT),
                "strategy": "asyncio aiohttp",
                "status": 0 if validated else -1,
                "error_msg": self.file_instance.error_msg,
                "local_path": self.file_instance.local_path,
                "process_name": "Controls (Size & checksum)",
            }
            print(
                "{},".format(result),
            )
