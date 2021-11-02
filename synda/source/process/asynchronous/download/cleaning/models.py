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

from synda.source.config.process.download.constants import TRANSFER

from synda.source.config.file.internal.models import Config as Internal
internal = Internal()

DOWNLOADING_LOGGER_NAME = internal.logger_consumer


class Process(object):

    def __init__(self, file_instance):

        # initializations
        self.file_instance = None

        self.file_instance = file_instance

    def init_metrics(self):
        self.file_instance.duration = None
        self.file_instance.rate = None

    def remove_local_path(self):
        full_local_path = self.file_instance.get_full_local_path()
        try:
            if os.path.exists(full_local_path):
                os.remove(
                    full_local_path,
                )
        except OSError:
            sdlog.error(
                "SDDMDEFA-158",
                "error occurs while removing local file ({})".format(
                    full_local_path,
                ),
                logger_name=DOWNLOADING_LOGGER_NAME,

            )

    def process(self):

        success = self.file_instance.status == TRANSFER["status"]['done']

        if not success:

            # A PROBLEM HAPPENED DURING DOWNLOAD

            # 1 / download target file is removed from disk

            self.remove_local_path()

            # 2 / unset metrics fields if transfer did not complete successfully

            self.init_metrics()

            self.file_instance.priority -= 1
