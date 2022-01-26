# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.models import Connection


def get_all_rows(full_filename=""):
    conn = Connection(full_filename=full_filename)
    manager = conn.get_item("dataset table crud").get_item("read")
    manager.set_db_connection(conn)
    data = manager.get_all_rows()
    conn.close()

    return data


if __name__ == '__main__':
    all_data = get_all_rows()
    pass
