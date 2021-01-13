# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


class DatabaseNotFound(Exception):
    def __init__(self, error):
        error_msg = "Database NOT FOUND / ERROR : '{}'"
        Exception.__init__(
            self,
            error_msg.format(
                error,
            ),
        )


class DataIntegrityError(Exception):
    def __init__(self, error):
        error_msg = "DATABASE INTEGRITY ERROR : '{}'"
        Exception.__init__(
            self,
            error_msg.format(
                error,
            ),
        )


class DataUnexpectedError(Exception):
    def __init__(self, error):
        error_msg = "DATABASE ERROR : '{}'"
        Exception.__init__(
            self,
            error_msg.format(
                error,
            ),
        )