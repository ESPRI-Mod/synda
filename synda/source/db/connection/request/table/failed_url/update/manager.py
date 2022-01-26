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
from synda.source.db.connection.request.table.dao.update.manager import Manager as Base

from synda.source.db.connection.request.table.failed_url.create.models import Table

from synda.source.db.connection.request.table.failed_url.update.models import InsertFailedUrl

table_name = Table().get_table_name()


class Manager(Base):

    def __init__(self):
        Base.__init__(self, table_name=table_name)
        self.set_data(
            [
                InsertFailedUrl(),

            ]
        )

    def insert_into_failed_url(self, url, file_functional_id, connection=None):
        request = self.get_item("insert_into_failed_url")
        return self.update(request, (url, file_functional_id), connection=connection)
