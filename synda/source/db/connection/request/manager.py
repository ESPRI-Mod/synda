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
from synda.source.manager import Manager as Base
from synda.source.db.connection.cursor.models import Cursor


class Manager(Base):

    def __init__(self, identifier):
        Base.__init__(self, identifier=identifier)
        # init
        self.db_connection = None

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    def get_db_connection(self):
        return self.db_connection

    def get_cursor(self):
        db_cursor = self.db_connection.get_cursor()
        if db_cursor:
            cursor = Cursor(
                db_cursor,
                db_identifier=self.db_connection.get_fullfilename(),
            )
        else:
            cursor = None

        return cursor
