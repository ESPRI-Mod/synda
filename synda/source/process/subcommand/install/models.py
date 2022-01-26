# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.subcommand.required.env.models import Process as Base


class Process(Base):

    def __init__(self, payload, arguments=None, exceptions_codes=None):
        super(Process, self).__init__(
            "install",
            payload,
            arguments=arguments,
            exceptions_codes=exceptions_codes,
        )

    def run(self, args):
        from synda.sdt import sdinstall
        status, newly_installed_files_count = sdinstall.run(
            args,
            self.get_payload().get_config(),
        )
        return status
