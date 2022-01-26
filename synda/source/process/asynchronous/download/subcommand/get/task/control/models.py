# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.sdt.sdtools import print_stderr

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
            print_stderr(
                'Warning: missing remote size attributes prevented file size verification ({})'.format(
                    self.file_instance.local_path,
                ),
            )
        return validated

    def validate_checksum(self, incorrect_checksum_action):
        validated, error_code, local_checksum = Base.validate_checksum(self, incorrect_checksum_action)

        if not validated:
            if error_code == "SDDMDEFA-160":
                print_stderr(
                    'Warning: missing remote checksum attributes prevented checksum verification ({})'.format(
                        self.file_instance.local_path,
                    ),
                )
            elif error_code == "SDDMDEFA-155" or error_code == "SDDMDEFA-157":
                print_stderr(
                    "Error: local checksum doesn't match remote checksum ({})".format(
                        self.file_instance.local_path,
                    ),
                )

        return validated
