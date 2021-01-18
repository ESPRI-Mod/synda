# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.table.models import Request


class Table(Request):
    """
        - 'realm' column is a group of keys/values (e.g. rtt, geo, etc..)
    """
    def __init__(self):
        super(Table, self).__init__("table", table_name="generic_cache")
        self.set_sql(
            "create table if not exists {} (realm TEXT, name TEXT, value TEXT)".format(
                self.get_table_name(),
            ),
        )
