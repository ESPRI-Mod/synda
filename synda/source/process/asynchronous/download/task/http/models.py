# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.process.asynchronous.download.task.models import Task as Base

preferences = Preferences()


class Task(Base):

    def __init__(self, file_instance, name, verbose=False):
        Base.__init__(self, file_instance, name, verbose=verbose)

    def get_client_session(self):
        return self.get_worker().get_manager().get_http_client_session()
