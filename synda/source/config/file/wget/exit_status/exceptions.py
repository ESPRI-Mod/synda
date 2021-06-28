# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
Useful for developers
"""


class InvalidExistStatus(Exception):
    def __init__(self, index, full_filename):
        error_msg = "INVALID WGET EXIT STATUS '{}' (Have a look at FILE : '{}')"
        Exception.__init__(
            self, error_msg.format(
                index,
                full_filename,
            ),
        )


class UnknownStatusError(Exception):
    def __init__(self, index, full_filename):
        error_msg = "Requested WGET EXIT STATUS : '{}' is NOT an entry of FILE : '{}'"
        Exception.__init__(
            self, error_msg.format(
                index,
                full_filename,
            ),
        )
