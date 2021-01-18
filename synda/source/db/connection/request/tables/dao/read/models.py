# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.source.db.connection.request.models import Request


class TableNames(Request):
    """
    Request

    """
    def __init__(self):
        super(TableNames, self).__init__(identifier="table names")
        self.set_sql(
            "SELECT * FROM sqlite_master WHERE type='table'",
        )


class IndexNames(Request):
    """
    Request

    """
    def __init__(self):
        super(IndexNames, self).__init__(identifier="index names")
        self.set_sql(
            "SELECT * FROM sqlite_master WHERE type='index'",
        )
