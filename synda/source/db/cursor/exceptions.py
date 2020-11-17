# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


class CursorNotAvailable(Exception):
    def __init__(self, identifier, error):
        error_msg = "NO CURSOR AVAILABLE / DATABASE IDENTIFIER : '{}' / ERROR : '{}'"
        Exception.__init__(
            self,
            error_msg.format(
                identifier,
                error,
            ),
        )
