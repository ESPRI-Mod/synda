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
from synda.source.db.connection.request.table.manager import TableName
from synda.source.db.connection.request.manager import Manager as Base


class Manager(Base, TableName):

    def __init__(self, table_name=""):
        TableName.__init__(self, table_name=table_name)
        Base.__init__(self, identifier="read")

    def get_request_data(self, request, args=None):
        request.set_cursor(self.get_cursor())
        data = None
        success = self.read(request, args=args)
        if success:
            data = request.get_data()
        request.close()
        return data

    def read(self, request, args=None):
        success = request.execute(args=args)
        return success
