# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.task.models import Task as Base


class Task(Base):

    def __init__(self):
        Base.__init__(self)

    async def process(self):
        await Base.process(self)
