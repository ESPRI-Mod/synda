# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.models import Connection
from synda.source.db.connection.request.tables.dao.create.manager import Manager as CreateManager


class Process(object):
    """
    Request

    """
    def __init__(self, full_filename=""):

        # init
        self.connection = None
        self.create_manager = None

        # settings
        self.connection = Connection(full_filename=full_filename)
        self.create_manager = CreateManager()

    def execute(self):

        self.create_manager.process(self.connection)
        return self.check()

    def check(self):
        expected_table_names = self.create_manager.get_table_names()
        read_tables_manager = self.connection.get_item("tables crud").get_item("read")
        read_tables_manager.set_db_connection(self.connection)
        table_names = read_tables_manager.get_table_names()
        assert sorted(table_names) == sorted(expected_table_names)

        index_names = read_tables_manager.get_index_names()
        expected_index_names = self.create_manager.get_index_names()
        assert sorted(index_names) == sorted(expected_index_names)
        return True
