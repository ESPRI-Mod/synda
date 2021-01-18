# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.request.models import Request as Base


class Request(Base):
    """
    Request

    """
    def __init__(self, identifier, table_name="", index_name=""):
        Base.__init__(self, identifier)

        # init
        self.table_name = ""
        self.index_name = ""

        # settings
        self.table_name = table_name
        self.index_name = index_name

    def get_table_name(self):
        return self.table_name

    def get_index_name(self):
        return self.index_name
