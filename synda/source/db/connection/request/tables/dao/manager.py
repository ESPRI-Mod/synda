# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
from synda.source.db.connection.request.manager import Manager as Base

from synda.source.db.connection.request.tables.dao.create.manager import Manager as CreateRequestsManager
from synda.source.db.connection.request.tables.dao.delete.manager import Manager as DeleteRequestsManager

from synda.source.db.connection.request.tables.dao.read.manager import Manager as ReadRequestsManager


class Manager(Base):

    def __init__(self):
        Base.__init__(self, "tables crud")
        self.add(
            CreateRequestsManager(),
        )
        self.add(
            ReadRequestsManager(),
        )
        self.add(
            DeleteRequestsManager(),
        )
