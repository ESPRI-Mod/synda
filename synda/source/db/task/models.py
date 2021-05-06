# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.source.db.connection.models import Connection
from synda.source.db.connection.request.tables.dao.create.manager import Manager as CreateManager


def check_db_schema(full_filename=""):

    conn = Connection(full_filename=full_filename, timeout=30)

    if os.path.exists(conn.get_fullfilename()):
        # tables creation
        tables_manager = CreateManager()
        expected_table_names = tables_manager.get_table_names()
        read_tables_manager = conn.get_item("tables crud").get_item("read")
        read_tables_manager.set_db_connection(conn)
        table_names = read_tables_manager.get_table_names()
        success = sorted(table_names) == sorted(expected_table_names)
        if success:
            index_names = read_tables_manager.get_index_names()
            expected_index_names = tables_manager.get_index_names()
            success = sorted(index_names) == sorted(expected_index_names)
        success = True
    else:
        success = False

    return success, conn.get_fullfilename()
