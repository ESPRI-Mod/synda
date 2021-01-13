# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


class NotFound(Exception):
    def __init__(self, full_filename):
        error_msg = "FILE NOT FOUND : '{}'"
        Exception.__init__(
            self, error_msg.format(
                full_filename,
            ),
        )


class FormatError(Exception):
    def __init__(self, full_filename):
        error_msg = "FILE FORMAT is Unknown : '{}'"
        Exception.__init__(
            self, error_msg.format(
                full_filename,
            ),
        )


class IndexError(Exception):
    def __init__(self, index, full_filename):
        error_msg = "REQUESTED index '{}' is NOT in FILE : '{}'"
        Exception.__init__(
            self, error_msg.format(
                index,
                full_filename,
            ),
        )


class InvalidIndex(Exception):
    def __init__(self, index, full_filename):
        error_msg = "REQUESTED index '{}' is NOT FOUND in FILE : '{}'"
        Exception.__init__(
            self, error_msg.format(
                index,
                full_filename,
            ),
        )
