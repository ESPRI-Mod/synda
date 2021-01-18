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
from synda.source.db.connection.request.manager import Manager as Base


class Manager(Base):
    """
        Manages request
    """
    def __init__(self, identifier):
        Base.__init__(self, identifier=identifier)

    def process(self, request, args=None):
        request.set_cursor(self.get_cursor())
        success = request.execute(args=args)
        request.close()
        return success
