# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import itertools


class Cursor(object):

    def __init__(self, cursor):
        self.cursor = cursor

    def get_database_cursor(self):
        return self.cursor

    def get_data(self):
        desc = self.cursor.description
        column_names = [col[0] for col in desc]

        return [
            dict(itertools.izip_longest(column_names, row)) for row in self.get_database_cursor().fetchall()
        ]


if __name__ == '__main__':

    import os
    from synda.bin.constants import ST_HOME
    from synda.source.db.connection.models import Connection

    full_filename = os.path.join(
        os.path.join(
            ST_HOME,
            "db",
        ),
        "sdt.db",
    )
    conn = Connection(full_filename)
    sql_request = "select version from version"
    conn.execute(sql_request)
    data = conn.get_cursor().get_data()
    conn.close()
    pass
