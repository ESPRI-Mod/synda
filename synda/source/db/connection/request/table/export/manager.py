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
from synda.source.db.connection.request.table.manager import Manager as Base

from synda.source.db.connection.request.table.export.create.manager import Manager as CreateManager
from synda.source.db.connection.request.table.export.read.manager import Manager as ReadManager


table_name = CreateManager().get_table_name()


class Manager(Base):

    def __init__(self):
        Base.__init__(self, identifier="{} table crud".format(table_name), table_name=table_name)
        self.add(
            CreateManager(),
        )
        self.add(
            ReadManager(),
        )
