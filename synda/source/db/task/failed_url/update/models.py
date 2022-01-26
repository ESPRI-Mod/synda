# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.models import Connection


def insert_into_failed_url(url, file_functional_id):
    conn = Connection()
    manager = conn.get_item("failed_url table crud").get_item("update")
    manager.set_db_connection(conn)
    success, lastrowid, msg = manager.insert_into_failed_url(url, file_functional_id, connection=conn)
    conn.close()

    return success, lastrowid, msg
