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


class TableName(object):

    def __init__(self, table_name=""):

        # init
        self.table_name = ""

        # settings
        self.table_name = table_name

    def get_table_name(self):
        return self.table_name


class Manager(Base, TableName):

    def __init__(self, identifier, table_name=""):
        Base.__init__(self, identifier=identifier)
        TableName.__init__(self, table_name=table_name)
