# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os


from synda.sdt import sdlog
from synda.sdt.sdtools import print_stderr

from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.file.internal.models import Config as Internal
from synda.source.process.asynchronous.download.task.control.models import Control as Base

internal = Internal()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

FILE_CORRUPTION_CHECKSUM_ERROR_MSG = "File corruption detected: local checksum doesn't match remote checksum"

DOWNLOADING_LOGGER_NAME = internal.logger_consumer


class Control(Base):

    def __init__(self, file_instance):
        Base.__init__(self, file_instance)

    def validate_file_size(self, local_file_size):
        validated, error_code = Base.validate_file_size(self, local_file_size)

        if not validated:
            error_msg = "size don't match (remote_size={}, local_size={}, local_path={})".format(
                int(self.file_instance.size),
                os.path.getsize(self.file_instance.get_full_local_path()),
                self.file_instance.get_full_local_path(),
            )

            sdlog.error(
                error_code,
                error_msg,
                logger_name=DOWNLOADING_LOGGER_NAME,
            )

            print_stderr(
                'Warning: missing remote size attributes prevented file size verification ({})'.format(
                    self.file_instance.local_path,
                ),
            )
        return validated

    def validate_checksum(self, incorrect_checksum_action):
        validated, error_code, local_checksum = Base.validate_checksum(self, incorrect_checksum_action)
        if not validated:
            if error_code == "SDDMDEFA-155":
                sdlog.error(
                    error_code,
                    "checksum doesn't match: "
                    "remove local file (local_checksum={}, remote_checksum={}, local_path={})".format(
                        local_checksum,
                        self.file_instance.checksum,
                        self.file_instance.get_full_local_path(),
                    ),
                    logger_name=DOWNLOADING_LOGGER_NAME,
                )

            elif error_code == "SDDMDEFA-157":
                sdlog.info(
                    error_code,
                    "local checksum doesn't match remote checksum ({})".format(
                        self.file_instance.get_full_local_path(),
                    ),
                    logger_name=DOWNLOADING_LOGGER_NAME,
                )

        return validated

    def update_log(self):

        if self.file_instance.status == TRANSFER["status"]['done']:
            sdlog.info(
                "SDDMDEFA-101",
                "Transfer done ({})".format(self.file_instance),
                logger_name=DOWNLOADING_LOGGER_NAME,
            )
        elif self.file_instance.status == TRANSFER["status"]['waiting']:
            # Transfer have been marked for retry
            #
            # This may happen for example
            #  - during shutdown immediate, where all running transfers are killed,
            # or when downloads are 'stalled' and killed by watchdog
            #  - as a consequence of sdnexturl

            sdlog.info(
                "SDDMDEFA-108",
                "Transfer marked for retry (error_msg='{}',url={},file_id={}".format(
                    self.file_instance.error_msg,
                    self.file_instance.url,
                    self.file_instance.file_id,
                ),
                logger_name=DOWNLOADING_LOGGER_NAME,
            )
        else:
            sdlog.info(
                "SDDMDEFA-102",
                "Transfer failed ({})".format(self.file_instance),
                logger_name=DOWNLOADING_LOGGER_NAME,
            )

    async def process(self, incorrect_checksum_action, local_file_size, local_checksum):
        await Base.process(self, incorrect_checksum_action, local_file_size, local_checksum)

        self.update_log()
