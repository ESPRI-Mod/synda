# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import asyncio

from synda.sdt import sdutils
from synda.sdt import sdlog
from synda.sdt import sdfiledao

from synda.sdt.sdexception import FatalException

from synda.source.config.file.constants import CHECKSUM
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.process.download.constants import TRANSFER

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
preferences = Preferences()

FILE_CORRUPTION_CHECKSUM_ERROR_MSG = "File corruption detected: local checksum doesn't match remote checksum"
DOWNLOAD_ERROR_MSG = "Error occured during download."


class Control(object):

    def __init__(self, file_instance):

        # initializations
        self.file_instance = None

        # settings
        self.file_instance = file_instance

    def file_size(self):
        is_correct = True
        if self.file_instance.size is not None:
            if int(self.file_instance.size) != os.path.getsize(self.file_instance.get_full_local_path()):
                is_correct = False
                sdlog.error(
                    "SDDMDEFA-002",
                    "size don't match (remote_size={}, local_size={}, local_path={})".format(
                        int(self.file_instance.size),
                        os.path.getsize(self.file_instance.get_full_local_path()),
                        self.file_instance.get_full_local_path(),
                    ),
                )

        return is_correct

    def file_checksum(self, incorrect_checksum_action=preferences.behaviour_incorrect_checksum_action):
        validated = True
        # retrieve remote checksum
        remote_checksum = self.file_instance.checksum

        if remote_checksum:
            # remote checksum exists

            # compute local checksum
            # fallback to 'md5' (arbitrary)

            checksum_type = self.file_instance.checksum_type if self.file_instance.checksum_type is not None else CHECKSUM['type']["md5"]
            local_checksum = sdutils.compute_checksum(self.file_instance.get_full_local_path(), checksum_type)

            # compare local and remote checksum
            if remote_checksum == local_checksum:
                # checksum is ok
                self.file_instance.status = TRANSFER["status"]['done']
                self.file_instance.error_msg = ""
            else:
                # checksum is not ok
                validated = False
                if incorrect_checksum_action == "remove":
                    self.file_instance.status = TRANSFER["status"]['error']
                    self.file_instance.priority -= 1
                    self.file_instance.error_msg = FILE_CORRUPTION_CHECKSUM_ERROR_MSG

                    # remove file from local repository
                    sdlog.error(
                        "SDDMDEFA-155",
                        "checksum don't match: "
                        "remove local file (local_checksum={}, remote_checksum={}, local_path={})".format(
                            local_checksum,
                            remote_checksum,
                            self.file_instance.get_full_local_path(),
                        ),
                    )

                elif incorrect_checksum_action == "keep":
                    sdlog.info(
                        "SDDMDEFA-157",
                        "local checksum doesn't match remote checksum ({})".format(
                            self.file_instance.get_full_local_path(),
                        ),
                    )

                    self.file_instance.status = TRANSFER["status"]['done']
                    self.file_instance.error_msg = ""
                else:
                    raise FatalException(
                        "SDDMDEFA-507",
                        "incorrect value ({})".format(incorrect_checksum_action),
                    )
        else:
            # remote checksum is missing
            # NOTE: we DON'T store the local checksum ('file' table contains only the *remote* checksum)

            self.file_instance.status = TRANSFER["status"]['done']
            self.file_instance.error_msg = ""

        return validated

    def _process(self):
        # 1 / file size must be the expected one
        self.file_size()
        # 1 / checksum must be correct
        self.file_checksum()

    def update_log(self):

        if self.file_instance.status == TRANSFER["status"]['done']:
            sdlog.info(
                "SDDMDEFA-101",
                "Transfer done ({})".format(self.file_instance),
            )
        elif self.file_instance.status == TRANSFER["status"]['waiting']:
            # Transfer have been marked for retry
            #
            # This may happen for example
            #  - during shutdown immediate, where all running transfers are killed,
            # or when wget are 'stalled' and killed by watchdog
            #  - as a consequence of sdnexturl

            sdlog.info(
                "SDDMDEFA-108",
                "Transfer marked for retry (error_msg='{}',url={},file_id={}".format(
                    self.file_instance.error_msg,
                    self.file_instance.url,
                    self.file_instance.file_id,
                ),
            )
        else:
            sdlog.info(
                "SDDMDEFA-102",
                "Transfer failed ({})".format(self.file_instance),
            )

    async def process(self):

        may_be_a_success = self.file_instance.sdget_status == 0 or self.file_instance.sdget_status is None
        if may_be_a_success:
            # MORE CONTROLS ARE REQUIRED TO BE SURE THAT NO PROBLEM OCCURED DURING DOWNLOAD
            await asyncio.to_thread(self._process)

        else:
            self.file_instance.status = TRANSFER["status"]['error']

        self.update_log()

        sdfiledao.update_file_after_download(self.file_instance)
