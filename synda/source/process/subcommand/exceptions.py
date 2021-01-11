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


class InvalidRequest(Exception):
    def __init__(self, strerror):
        error_msg = "Not found {}"
        Exception.__init__(
            self,
            error_msg.format(
                strerror,
            ),
        )


class NotAuthorized(Exception):
    def __init__(self, strerror):
        error_msg = "Authorization refused : esgf {}"
        Exception.__init__(
            self,
            error_msg.format(
                strerror,
            ),
        )


class ProcessNotImplemented(Exception):
    def __init__(self, sub_command_name):
        error_msg = "The class name of the '{}' sub-command process is required " \
                    "by the manager of the sub-command processes"
        Exception.__init__(
            self,
            error_msg.format(
                sub_command_name,
            ),
        )
