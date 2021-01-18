# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.identifier import Identifier


class Request(Identifier):
    """
    Request

    """
    def __init__(self, identifier=""):
        Identifier.__init__(self, identifier)
        self.cursor = None
        self.sql = ""

    def set_cursor(self, cursor):
        self.cursor = cursor

    def close(self):
        self.cursor.close()

    def execute(self, args=None):
        success = self.cursor.execute(self.get_sql(), args=args)
        return success

    def get_sql(self):
        return self.sql

    def set_sql(self, sql):
        self.sql = sql

    def get_data(self):
        return self.cursor.get_data()
