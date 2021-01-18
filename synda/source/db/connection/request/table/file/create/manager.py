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
from synda.source.db.connection.request.table.dao.create.manager import Manager as Base

from synda.source.db.connection.request.table.file.create.models import Table

from synda.source.db.connection.request.table.file.create.models import IndexOnFilename
from synda.source.db.connection.request.table.file.create.models import IndexOnModel
from synda.source.db.connection.request.table.file.create.models import IndexOnFileFunctionalId
from synda.source.db.connection.request.table.file.create.models import IndexOnCreaDate
from synda.source.db.connection.request.table.file.create.models import IndexOnProject
from synda.source.db.connection.request.table.file.create.models import IndexOnChecksum
from synda.source.db.connection.request.table.file.create.models import IndexOnDatasetId
from synda.source.db.connection.request.table.file.create.models import IndexOnInsertionGroupId
from synda.source.db.connection.request.table.file.create.models import IndexOnLocalPath
from synda.source.db.connection.request.table.file.create.models import IndexOnPriority
from synda.source.db.connection.request.table.file.create.models import IndexOnStatus
from synda.source.db.connection.request.table.file.create.models import IndexOnTrackingId


table_name = Table().get_table_name()


class Manager(Base):

    def __init__(self):
        Base.__init__(self, table_name=table_name)
        self.set_data(
            [
                Table(),

                # indexes

                IndexOnFilename(),
                IndexOnModel(),
                IndexOnFileFunctionalId(),
                IndexOnTrackingId(),
                IndexOnStatus(),
                IndexOnPriority(),
                IndexOnInsertionGroupId(),
                IndexOnProject(),
                IndexOnLocalPath(),
                IndexOnDatasetId(),
                IndexOnCreaDate(),
                IndexOnChecksum(),
            ]
        )
