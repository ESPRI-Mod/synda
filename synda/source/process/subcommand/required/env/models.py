# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.subcommand.models import Process as Base


class Process(Base):

    def __init__(self, name, authority, arguments=None, exceptions_codes=None):
        super(Process, self).__init__(
            name,
            authority,
            is_environment_required=True,
            arguments=arguments,
            exceptions_codes=exceptions_codes,
        )
