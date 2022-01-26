# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.source.process.asynchronous.download.task.models import Task as Base


class Task(Base):

    def __init__(self, file_instance, name, process_cls, control_cls=None, verbose=False):
        Base.__init__(self, file_instance, name, process_cls, control_cls=control_cls, verbose=verbose)
        self.progression = dict(
            filename="",
            current_size=0,
            rate=0.0,
            expected_size=0,
            percentage=0,
        )

    def get_progression(self):

        local_path = self.file_instance.get_full_local_path()
        filename = self.file_instance.filename \
            if self.file_instance.filename else os.path.basename(local_path)

        res = self.progression
        res["filename"] = filename
        res["expected_size"] = self.file_instance.size
        res["data_node"] = self.file_instance.data_node
        res["start_date"] = self.file_instance.start_date
        res["status"] = self.status

        return self.progression
