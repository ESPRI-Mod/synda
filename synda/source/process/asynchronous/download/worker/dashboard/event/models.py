# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.worker.dashboard.event.models import Event as Base


class Event(Base):

    def __init__(self, dashboord):
        Base.__init__(self, dashboord)

    def new_task_status(self, task):
        Base.new_task_status(self, task)

