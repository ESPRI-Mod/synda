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


class MethodNotImplemented(Exception):
    def __init__(self, method_name, class_name):
        error_msg = "Please, Implement the '{}' method for '{}'"
        Exception.__init__(
            self,
            error_msg.format(
                method_name,
                class_name,
            ),
        )


class FileNotFound(Exception):
    def __init__(self, full_filename):
        error_msg = "FILE NOT FOUND : '{}'"
        Exception.__init__(
            self, error_msg.format(
                full_filename,
            ),
        )


class FileFormatError(Exception):
    def __init__(self, full_filename):
        error_msg = "FILE FORMAT is Unknown : '{}'"
        Exception.__init__(
            self, error_msg.format(
                full_filename,
            ),
        )
