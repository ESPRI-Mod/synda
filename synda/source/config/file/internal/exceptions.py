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


class NotFound(Exception):
    def __init__(self, filename, directory):
        error_msg = "'{}' is required in the '{}' directory of th synda environment (built by init-env sub command)"
        Exception.__init__(
            self,
            error_msg.format(
                filename,
                directory
            ),
        )
