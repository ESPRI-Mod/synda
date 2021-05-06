# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.models import Connection
from synda.source.containers import Container


class Task(Container):

    def __init__(self, db_file=""):
        super(Task, self).__init__(identifier="create failed_url task")
        # init
        self.nb_db_access = 0
        self.connection = None
        self.manager = None
        self.cursor = None

        # settings
        self.connection = Connection(full_filename=db_file)
        self.manager = self.connection.get_item("failed_url table crud").get_item("create")
        self.manager.set_db_connection(self.connection)
        self.cursor = self.manager.get_cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

