# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.subcommand.models import SubCommand as Base


class SubCommand(Base):

    def __init__(self, context, exceptions_codes=None, description=""):
        super(SubCommand, self).__init__(
            "getinfo",
            context,
            exceptions_codes=exceptions_codes,
            description="Getinfo subcommand Context",
        )
        print(context.get_file())
        self.configure(
            context.get_file().get_filename(),
        )

    def configure(self, filename):

        self.set_argv(
            ['synda', self.name, "--filesize", filename],
        )
