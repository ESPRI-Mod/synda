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


class ProcessStopped(Exception):
    def __init__(self):
        error_msg = "Downloads have been stopped by user"
        Exception.__init__(
            self,
            error_msg,
        )
