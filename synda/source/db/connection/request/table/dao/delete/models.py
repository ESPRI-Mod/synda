# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.request.table.models import Request as Base


class Drop(Base):
    """
    Request

    """
    def __init__(self):
        Base.__init__(self, "drop")
        self.set_sql(
            "DROP TABLE {}",
        )

    def execute(self, args=None):
        sql = self.get_sql().format(
            args[0],
        )
        success = self.cursor.execute(sql)
        return success
