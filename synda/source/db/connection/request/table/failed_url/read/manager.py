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
from synda.source.db.connection.request.table.dao.read.manager import Manager as Base
from synda.source.db.connection.request.table.failed_url.read.models import AllRows as AllRowsRequest


table_name = "failed_url"


class Manager(Base):

    def __init__(self):
        Base.__init__(self, table_name=table_name)
        self.add(
            AllRowsRequest(),
        )

    def get_all_rows(self, limit=None):
        request = self.get_item("all rows")
        if limit:
            res = self.get_request_data(request, (limit,))
        else:
            res = self.get_request_data(request)
        return res
